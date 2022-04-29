from fastapi import File
import psycopg2
# Get data with Dict
import psycopg2.extras

import sys
from config.settings import settings

def get_conn(db : str):
    conn= psycopg2.connect(user=settings.POSTGRES_USER,
                                  password=settings.POSTGRES_PASSWORD,
                                  host=settings.POSTGRES_HOST,
                                  port=settings.POSTGRES_PORT,
                                  database=db)

    
    return conn



  



"""
def get_file_id(id:str,conn):
    psycopg2.extras.register_uuid()
   
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            params = (id,)
            sql ="select f.id, f.entrydate, f.hash, f.path,f.originalname, f.size,entity,f.entityid, c.format as ext, c.mimetype
                    from arc_file f
                    inner join arc_contenttype c on f.contenttype_id = c.id
                    where c.deleted= false
                    and f.id = %s"
          
            cursor.execute(sql,params)
            row = cursor.fetchone()
            #row['id']= str(row['id']) -- esto antes de usar pydantic, typing como debe ser
    
    except psycopg2.DatabaseError as e:
        row=None ## responder Null
        if conn:
            conn.rollback()
        
        #print(f'Error {e}') ### esto rompe la app mas arriba
        #sys.exit(1)

    
    return row   


def get_file(name:str,conn):

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            params = (name,)
            sql ="select f.id, f.entrydate, f.hash, f.path,f.originalname, 
                    f.size,entity,f.entityid, c.format as ext, c.mimetype
                    from arc_file f
                    inner join arc_contenttype c on f.contenttype_id = c.id
                    where c.deleted= false and f.path = %s
                    "
            cursor.execute(sql,params)
            row = cursor.fetchone()
           
    
    except psycopg2.DatabaseError as e:

        if conn:
            conn.rollback()

        print(f'Error {e}')
        sys.exit(1)

    
    return row   

def get_allfiles(conn):
    
   
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
   
    conn=get_conn('sifincactg')
    #row= get_file('/tmp/php2tEtHq',conn)

    files = get_allfiles(conn)
    path = '/tmp/phpKaROgw'
    
    res = next((x for x in files if x[1] == path), None)
   
    print(res)


"""



if __name__=='__main__':
   pass

