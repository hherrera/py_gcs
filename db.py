from dotenv import load_dotenv
import psycopg2
# Get data with Dict
import psycopg2.extras
import sys
import os

def get_conn():
    conn= psycopg2.connect(user=os.getenv('USER'),
                                  password=os.getenv('PASSWORD'),
                                  host=os.getenv('HOST'),
                                  port=os.getenv('PORT'),
                                  database=os.getenv('DATABASE'))

    
    return conn



def get_file(name : str,conn):
    
    """ Query file from the 'arc_file' table for name"""
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            params = (name,)
            sql ="SELECT * FROM arc_file f WHERE f.path = %s"
            cursor.execute(sql,params)
            row = cursor.fetchone()
            
    
    except psycopg2.DatabaseError as e:

        if conn:
            conn.rollback()

        print(f'Error {e}')
        sys.exit(1)

    
    return row   

def get_allfiles(conn):
    
    """ Query  all files from the 'arc_file' table for name"""
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            sql ="SELECT id, path FROM arc_file f WHERE deleted = false order by path"
            cursor.execute(sql)
            row = cursor.fetchall()
            
    
    except psycopg2.DatabaseError as e:

        if conn:
            conn.rollback()

        print(f'Error {e}')
        sys.exit(1)

    
    return row  


if __name__=='__main__':
    load_dotenv()
    conn=get_conn()
    files= get_allfiles(conn)
    path = '/tmp/phpKaROgw'
    #res = next(filter(lambda x: x[1]==path,files))
    res = next((x for x in files if x[1] == path), None)
   
    print(res)

