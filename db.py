from dotenv import load_dotenv
import psycopg2
import os
def get_conn():
    conn= psycopg2.connect(user=os.getenv('USER'),
                                  password=os.getenv('PASSWORD'),
                                  host=os.getenv('HOST'),
                                  port=os.getenv('PORT'),
                                  database=os.getenv('DATABASE'))

    
    return conn

def get_file(name : str):
    
    """ Query file from the files table for name"""
    conn=None
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM arc_file WHERE filename =%",(name,))
        row = cur.fetchone()
       
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            cur.close()
            conn.close()


if __name__=='__main__':
    load_dotenv()
    f= get_file('phpCWV3sI')
    print(f)

