import sqlite3, os
from sqlite3 import Error

def create_coin_connection():
    conn = None
    try:
        conn = sqlite3.connect(os.path.join('db','ergicoin.sqlite'))
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)
    
    if conn:
        return conn

def close_coin_connection(conn):
    conn.commit()
    conn.close()
    print("connection closed")

def create_money_table(conn):
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

def initialize_user_money(conn, username, userid):
    if not user_exists_in_money_table(conn, userid):
        sql = ''' INSERT INTO money(username, userid, coins)
                VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (username, userid, 1000))
        conn.commit()
        return cur.lastrowid
    return None

def update_user_money(conn, userid, new_money):
    sql = ''' UPDATE money
              SET coins = ?
              WHERE userid = ?'''
    cur = conn.cursor()
    cur.execute(sql, (new_money, userid))
    conn.commit()

def user_exists_in_money_table(conn, userid):
    sql = ''' SELECT * FROM money WHERE userid=? '''
    cur = conn.cursor()
    cur.execute(sql, (userid,))
    rows = cur.fetchall()

    return len(rows) > 0

def get_user_money(conn, userid, username=None):
    if username != None:
        if not user_exists_in_money_table(conn, userid):
            initialize_user_money(conn, username, userid)

    sql = ''' SELECT coins FROM money WHERE userid=? '''
    cur = conn.cursor()
    cur.execute(sql, (userid,))
    money = cur.fetchone()

    if money is not None:
        return money[0]
    else:
        return None
    
def print_all_tables(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cur.fetchall())

def transfer_coins(conn, from_userid, to_userid, amount):
    from_user_money = get_user_money(conn, from_userid)
    to_user_money = get_user_money(conn, to_userid)

    if from_user_money is None or to_user_money is None:
        return False  # One of the users does not exist in the table

    if from_user_money < amount:
        return False  # Not enough coins

    update_user_money(conn, from_userid, from_user_money - amount)
    update_user_money(conn, to_userid, to_user_money + amount)

    return True

def modify_wallet(conn, username, userid, amount):
    user_money = get_user_money(conn, userid, username)
    
    if (user_money + amount) < 0:
        return False
    
    update_user_money(conn, userid, user_money + amount)
    
    return True

conn = create_coin_connection()
create_money_table(conn)
close_coin_connection(conn)
