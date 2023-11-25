# Требуется хранить персональную информацию о клиентах:

# имя,
# фамилия,
# email,
# телефон.


import sqlite3


def create_db_structure():
    conn = sqlite3.connect('client_management.db')
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
    conn.commit()
    conn.close()


def add_new_client(first_name, last_name, email, additional_info=None):
    conn = sqlite3.connect('client_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clients (first_name, last_name, email, additional_info)
        VALUES (?, ?, ?, ?)
    ''', (first_name, last_name, email, additional_info))
    conn.commit()
    conn.close()


def add_phone_for_client(client_id, phone_number):
    conn = sqlite3.connect('client_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE clients
        SET additional_info = COALESCE(additional_info || ', ' || ?, ?)
        WHERE id = ?
    ''', (phone_number, phone_number, client_id))
    conn.commit()
    conn.close()


def update_client_info(client_id, new_email):
    conn = sqlite3.connect('client_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE clients
        SET email = ?
        WHERE id = ?
    ''', (new_email, client_id))
    conn.commit()
    conn.close()

def delete_phone_for_client(client_id, phone_number):
    conn = sqlite3.connect('client_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE clients
        SET additional_info = REPLACE(additional_info, ?, '')
        WHERE id = ?
    ''', (phone_number, client_id))
    conn.commit()
    conn.close()

def delete_client(client_id):
    conn = sqlite3.connect('client_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM clients
        WHERE id = ?
    ''', (client_id,))
    conn.commit()
    conn.close()


def find_client(search_term):
    conn = sqlite3.connect('client_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE first_name = ? OR last_name = ? OR email = ? OR additional_info LIKE ?', (search_term, search_term, search_term, f'%{search_term}%'))
    result = cursor.fetchall()
    conn.close()
    return result

# Тест
create_db_structure()
add_new_client('Иван', 'Иванов', 'ivan@example.com')
add_phone_for_client(1, '123-456-7890')
update_client_info(1, 'ivan_updated@example.com')
find_client('Иван')
delete_phone_for_client(1, '123-456-7890')
delete_client(1)
