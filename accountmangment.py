import sqlite3
import random

# Connect to the SQLite database
def load():
    conn = sqlite3.connect('acc.db')
    cursor = conn.cursor()

    # Create a table for demonstration purposes (if not exists)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    return cursor,conn

def get_random_accounts( n=101):
    cursor,conn =load()
    cursor.execute('SELECT id, password FROM accounts')
    accounts = cursor.fetchall()
    if len(accounts) > n:
        accounts = random.sample(accounts, n)
    return accounts

def get_random_account( n=2):
    cursor,conn =load()
    cursor.execute('SELECT id, password FROM accounts')
    accounts = cursor.fetchall()
    if len(accounts) > n:
        accounts = random.sample(accounts, n)
    return accounts

def delete_account_by_id( account_id):
    cursor,conn =load()
    cursor.execute('DELETE FROM accounts WHERE id = ?', (account_id,))
    conn.commit()

# Example usage for getting random accounts
 
 
 