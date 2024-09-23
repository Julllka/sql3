import psycopg2

with psycopg2.connect(database="netology_hw", user="postgres", password="postgres") as conn:
    cur = conn.cursor()

def create_db(conn):
    cur.execute("""CREATE TABLE IF NOT EXISTS customer(
    customer_id SERIAL PRIMARY KEY, 
    first_name VARCHAR(40) NOT NULL,
    second_name VARCHAR(40) NOT NULL,
    email VARCHAR(15) UNIQUE,
    phone VARCHAR(15) UNIQUE
    );""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phonenumbers(
    number VARCHAR(11) PRIMARY KEY,
    customer_id INTEGER REFERENCES customer(id)
    );
    """)
    return

def add_client(conn, first_name, last_name, email, phone=None):
    cur.execute("""
    INSERT INTO customer(first_name, last_name, email)
    VALUES (%s, %s, %s)
    """, (first_name, last_name, email))
    cur.execute("""
           SELECT id from clients
           ORDER BY id DESC
           LIMIT 1
           """)
    id = cur.fetchone()[0]
    if phone is None:
        return id
    else:
        add_phone(conn, customer_id, phone)
        return customer_id


def add_phone(conn, customer_id, phone):
    cur.execute("""
    INSERT INTO phonenumbers(number, customer_id) 
    VALUES(%s, %s)
    """, (phone, customer_id))
    return customer_id


def change_client(conn, customer_id, first_name=None, last_name=None, email=None, phones=None):
    cur.execute("""
    SELECT * from customer
        WHERE customer_id = %s
        """, (customer_id, ))
    info = cur.fetchone()
    if first_name is None:
        first_name = info[1]
    if last_name is None:
        last_name = info[2]
    if email is None:
        email = info[3]
    cur.execute("""
        UPDATE customer
        SET first-name = %s, last_name = %s, email =%s 
        WHERE customer_id = %s
        """, (first_name, last_name, email, customer_id))
    return customer_id

def delete_phone(conn, customer_id, phone):
    cur.execute("""
    DELETE FROM phonenumbers WHERE number = %s
    """, (number, ))
    return number

def delete_client(conn, customer_id):
    cur.execute("""
    DELETE FROM phonenumbers
    WHERE customer_id = %s
    """, (customer_id,))
    cur.execute("""
    DELETE FROM customer WHERE customer_id = %s
    """, (customer_id, ))
    return customer_id

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    if first_name is None:
        first_name = '%'
    else:
        first_name = '%' + first_name + '%'
    if last_name is None:
        last_name = '%'
    else:
        last_name = '%' + last_name + '%'
    if email is None:
        email = '%'
    else:
        email = '%' + email + '%'
    if phone is None:
        cur.execute("""
                SELECT c.id, c.first_name, c.last_name, c.email, p.number FROM customer c
                LEFT JOIN phonenumbers p ON c.id = p.customer_id
                WHERE c.first_name LIKE %s AND c.last_name LIKE %s
                AND c.email LIKE %s
                """, (first_name, last_name, email))
    else:
        cur.execute("""
                SELECT c.id, c.first_name, c.last_tname, c.email, p.number FROM customer c
                LEFT JOIN phonenumbers p ON c.id = p.customer_id
                WHERE c.first_name LIKE %s AND c.last_name LIKE %s
                AND c.email LIKE %s AND p.number like %s
                """, (first_name, last_name, email, phone))
    return cur.fetchall()


conn.close()