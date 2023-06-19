import sqlite3, os
from sqlite3 import Error

import shutil
import datetime

def store_backup_date(conn):
    date = datetime.datetime.now().isoformat()
    sql = ''' INSERT INTO backups(date) VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (date,))
    conn.commit()
    return cur.lastrowid

def retrieve_latest_backup_date(conn):
    sql = ''' SELECT * FROM backups ORDER BY date DESC LIMIT 1 '''
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    if rows:
        return datetime.datetime.fromisoformat(rows[0][1])
    else:
        return None

def backup_database():
    backup_dir = os.path.join('db', 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    backup_file = os.path.join(backup_dir, f'ergibot_db_backup_{datetime.datetime.now().isoformat().replace(":", "-")}.sqlite')
    shutil.copy2(os.path.join('db', f'ergibot_db.sqlite'), backup_file)

def check_and_perform_backup(conn):
    create_tables(conn)
    last_backup_date = retrieve_latest_backup_date(conn)

    if last_backup_date is None or (datetime.datetime.now() - last_backup_date).total_seconds() >= 24 * 3600:
        print("backing up db...")
        backup_database()
        store_backup_date(conn)

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect(os.path.join('db','ergibot_db.sqlite'))
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)

    if conn:
        create_tables(conn)
        return conn

def close_connection(conn):
    conn.commit()
    check_and_perform_backup(conn)
    conn.close()
    print(f"connection closed")

def get_row_index():
    return {
        "id"             : 0,
        "username"       : 1,
        "userid"         : 2,
        "date"           : 3,
        "entry"          : 4,
        "key"            : 5,
        "file_extension" : 6,
        "file_type"      : 7,
        "local_path"     : 8,
        "type"           : 9,
        "language"       : 10
    }

def create_tables(conn):
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
                                            type text NOT NULL,
                                            language text
                                        );"""
        conn.execute(sql_create_table)
    except Error as e:
        print(e)

    try:
        sql_create_table = """CREATE TABLE IF NOT EXISTS money (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            username text NOT NULL,
                                            userid text NOT NULL,
                                            coins int NOT NULL DEFAULT 1000
                                        );"""
        conn.execute(sql_create_table)
    except Error as e:
        print(e)

    try:
        sql_create_table = """CREATE TABLE IF NOT EXISTS backups (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            date text NOT NULL
                                        );"""
        conn.execute(sql_create_table)
    except Error as e:
        print(e)

def store_entry(conn, entry):
    sql = ''' INSERT INTO entries(username,userid,date,entry,key,file_extension,file_type,local_path,type,language)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
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

def delete_entry(conn, key):
    sql = ''' DELETE FROM entries WHERE key=? '''
    cur = conn.cursor()
    cur.execute(sql, (key,))
    conn.commit()
    cur.close()
