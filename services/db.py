from fastapi import File
import psycopg2
# Get data with Dict
import psycopg2.extras

import sys
from config.settings import settings
from config.handler_logging import logger

def get_conn(db : str):
    
    try:
        conn= psycopg2.connect(user=settings.POSTGRES_USER,
                                  password=settings.POSTGRES_PASSWORD,
                                  host=settings.POSTGRES_HOST,
                                  port=settings.POSTGRES_PORT,
                                  database=db)
    except (psycopg2.DatabaseError,psycopg2.OperationalError) as e:
        conn=None ## responder Null
        logger.log_text(f'Error {e}', severity="ERROR")
        raise
    return conn




if __name__=='__main__':
   pass

