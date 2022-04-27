import time

from config.settings import settings
from services.gcs  import  list_blobs, mv_blob
from services.db import get_allfiles,get_file, get_conn

def debug_blob(db_name, bucket_name,bucket_name_dest, folder_dest,limit=0, pretend =True):
    n=0
    size=0
    nofound=[]
    
    print(f'Cargando todos los blobs de {bucket_name}')
    blobs = list_blobs(bucket_name)
    
      #buscar blob en la base de datos 
    print(f'Conectandose a {db_name}')
    conn = get_conn(db_name)
    
    print(f'Cargando datos de {db_name}...')
    files=get_allfiles(conn)
    nreg = len(files)
    print(f'{nreg} registros cargados')
    for blob in blobs:
        n += 1 
        print(f'[{n}]Procesando blob {blob.name}')

        file = next((x for x in files if x[1] == blob.name), None)
         # Not found file - erase o move blob
        if file is None:
            print(f'{blob.name} no fue encontrado')
            nofound.append(blob.name)

            f= blob.name.split('/')  
            dest= folder_dest+'/'+f[len(f)-1]              
            
            ### validate pretend
            if not pretend:
                mv_blob(bucket_name, blob.name,bucket_name_dest,dest )
                print(f'{blob.name} fue movido a {dest}')
            size+=blob.size 
        else:
            print(f" --- > Id: {file[0]} / Path: {file[1]}")
        if limit:
            if n==limit:
                break
    return nofound,n,size

def debug_blob_1x1(db_name, bucket_name, bucket_name_dest,folder_dest):
    n=0
    size=0
    nofound=[]
    
    print(f'Cargando todos los blobs de {bucket_name}')
    blobs = list_blobs(bucket_name)
    
      #buscar blob en la base de datos 
    print(f'Conectandose a {db_name}')
    conn = get_conn(db_name)
    for blob in blobs:
        n += 1 
        print(f'[{n}]Procesando blob {blob.name}')

        file = get_file(blob.name,conn)
         # Not found file - erase o move blob
        if file is None:
            print(f'{blob.name} no fue encontrado')
            nofound.append(blob.name)

            f= blob.name.split('/')  
            dest= folder_dest+'/'+f[len(f)-1]              
            
            mv_blob(bucket_name, blob.name,bucket_name_dest,dest)
            print(f'{blob.name} fue movido a {dest}')
            size+=blob.size 
        else:
            print(f" --- > ID: {file['id']} / Path: {file['path']}")
        
        if n==10:
            break
    return nofound,n,size

if __name__=='__main__':
    pass