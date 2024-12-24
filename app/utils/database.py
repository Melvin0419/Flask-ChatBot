import psycopg2
from dotenv import load_dotenv
import os

def get_connection():

    try:
        conn = psycopg2.connect(
            dbname="flask_db",
            user="postgres",
            password=os.getenv('DB_PASSWORD'),
            host="localhost",
            port=5432
        )
        return conn
    
    except psycopg2.Error as e:
        print(f'ERROR:{e}')
        return None

def insert_user(username):
    # 建立DB連結
    conn = get_connection()
    if conn:
        try:
            # 建立 cursor 來執行SQL
            cursor = conn.cursor()
            query = "INSERT INTO users (username) VALUES (%s) RETURNING id;"
            cursor.execute( query,(username,))
            # 提交變更
            conn.commit()
            # 取得 user_id
            user_id = cursor.fetchone()[0]
            print(f'User is created with id:{user_id}')
        except psycopg2.Error as e:
            print(f'ERROR:{e}')
            # 回復動作
            conn.rollback()
        finally:
            # 關閉連結
            cursor.close()
            conn.close()
            return user_id

def insert_message(user_id,role,message):

    conn = get_connection()

    if conn:

        try:
            cursor = conn.cursor()
            query = "INSERT INTO conversations (user_id, role, message) VALUES (%s,%s,%s);"
            cursor.execute(query,(user_id,role,message,))
            # 提交變更
            conn.commit()
            print('INSERT Message!')
        except psycopg2.Error as e:
            print(f'ERROR:{e}')
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def get_conversation(username):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = f'''

            SELECT conversations.role, conversations.message
            FROM conversations
            JOIN users
            ON conversations.user_id = users.id
            WHERE username = '{username}'
            ORDER BY timestamp;

            '''
            cursor.execute(query)
            conversation = cursor.fetchall()
            print('Retrieve conversation!')
            
        except psycopg2.Error as e:
            print(f'ERROR:{e}')
        
        finally:
            cursor.close()
            conn.close()
            return conversation

def get_userid(username):
    conn = get_connection()
    userid=None
    if conn:
        try:
            cursor = conn.cursor()
            query = f'''
            SELECT id
            FROM users
            WHERE username = '{username}'
            '''
            cursor.execute(query)
            userid = cursor.fetchone()[0]
            
        except psycopg2.Error as e:
            print(f'ERROR:{e}')
        
        finally:
            cursor.close()
            conn.close()
            return userid

if get_userid('melvin'):
    print('yse')