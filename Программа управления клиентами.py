# Требуется хранить персональную информацию о клиентах:

# имя,
# фамилия,
# email,
# телефон.




import sqlite3


def create_db_structure():
    with sqlite3.connect('client_management.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                additional_info TEXT
            )
        ''')


def add_new_client(first_name, last_name, email, additional_info=None):
    with sqlite3.connect('client_management.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clients (first_name, last_name, email, additional_info)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, email, additional_info))


def update_client_info(client_id, first_name=None, last_name=None, email=None, additional_info=None):
    with sqlite3.connect('client_management.db') as conn:
        cursor = conn.cursor()
        fields = []
        params = []

        if first_name is not None:
            fields.append("first_name = ?")
            params.append(first_name)
        if last_name is not None:
            fields.append("last_name = ?")
            params.append(last_name)
        if email is not None:
            fields.append("email = ?")
            params.append(email)
        if additional_info is not None:
            fields.append("additional_info = ?")
            params.append(additional_info)

        params.append(client_id)
        sql = f"UPDATE clients SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(sql, params)


def find_client(first_name=None, last_name=None, email=None, additional_info=None):
    with sqlite3.connect('client_management.db') as conn:
        cursor = conn.cursor()
        fields = []
        params = []
        
        for field, value in zip(['first_name', 'last_name', 'email', '%additional_info%'], [first_name, last_name, email, additional_info]):
            if value is not None:
                fields.append(f"{field} = ?")
                params.append(value)

        sql = f"SELECT * FROM clients WHERE {' AND '.join(fields)}"
        cursor.execute(sql, params)
        return cursor.fetchall()


if __name__ == "__main__":
    create_db_structure()
    add_new_client('Иван', 'Иванов', 'ivan@example.com')
    update_client_info(client_id=1, email='ivan_updated@example.com', additional_info='New info')
    found_clients = find_client(first_name='Иван')
    print(found_clients)

