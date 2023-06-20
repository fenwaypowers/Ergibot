import sqlite3, os
from sqlite3 import Error
from database import *

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
    if new_money == 0:
        new_money = 1000
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

    if money[0] == 0:
        update_user_money(conn, userid, 0)
        return 1000
    elif money is not None:
        return money[0]
    else:
        return None

def transfer_coins(conn, from_userid, to_userid, amount):
    from_user_money = get_user_money(conn, from_userid)
    to_user_money = get_user_money(conn, to_userid)

    if from_user_money is None or to_user_money is None:
        return False  # One of the users does not exist in the table

    if from_user_money < amount:
        return False  # Not enough coins
    
    if from_user_money - amount < 1000:
        return False # Ensures user will have at least 1000 coins after transfer.

    update_user_money(conn, from_userid, from_user_money - amount)
    update_user_money(conn, to_userid, to_user_money + amount)

    return True

def modify_wallet(conn, username, userid, amount):
    user_money = get_user_money(conn, userid, username)
    
    if (user_money + amount) < 0:
        return False
    
    update_user_money(conn, userid, user_money + amount)
    
    return True

def validate_bet(user_money, bet):
    return user_money < bet or bet < 0
