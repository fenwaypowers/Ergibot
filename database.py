import sqlite3, os
from sqlite3 import Error

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect(os.path.join('db','ergibot_db.sqlite'))
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)
    
    if conn:
        return conn

def close_connection(conn):
    conn.commit()
    conn.close()
    print("connection closed")

def get_row_index():
    return {
        "id" : 0,
        "username": 1,
        "userid" : 2,
        "date" : 3,
        "entry" : 4,
        "key" : 5,
        "file_extension" : 6,
        "file_type" : 7,
        "local_path" : 8,
        "type" : 9
    }

def create_entries_table(conn):
    try:
        sql_create_table = """CREATE TABLE IF NOT EXISTS entries (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            username text NOT NULL,
                                            userid text NOT NULL,
                                            date text NOT NULL,
                                            entry text NOT NULL,
                                            key text NOT NULL,
                                            file_extension text,
                                            file_type text,
                                            local_path text,
                                            type text NOT NULL
                                        );"""
        conn.execute(sql_create_table)
    except Error as e:
        print(e)

def store_entry(conn, entry):
    sql = ''' INSERT INTO entries(username,userid,date,entry,key,file_extension,file_type,local_path,type)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, entry)
    conn.commit()
    return cur.lastrowid

def retrieve_link(conn, key):
    sql = ''' SELECT * FROM entries WHERE key=? '''
    cur = conn.cursor()
    cur.execute(sql, (key,))
    rows = cur.fetchall()
    return rows

def select_all_links(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM entries")
    rows = cur.fetchall()
    for row in rows:
        print(row)
        
def key_exists(conn, key):
    sql = ''' SELECT * FROM entries WHERE key=? '''
    cur = conn.cursor()
    cur.execute(sql, (key,))
    rows = cur.fetchall()

    return len(rows) > 0

conn = create_connection()
create_entries_table(conn)
close_connection(conn)
