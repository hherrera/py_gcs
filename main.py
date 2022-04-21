from webbrowser import get
from dotenv import load_dotenv
from pkg_resources import resource_string
from services.gcs  import  list_blobs, del_blob, mv_blob, blob_metadata
from db import  get_file,get_allfiles, get_conn

def main():
    # load .env
    bucket_name ='sifinca-files'
    load_dotenv()

    #d=get_blob_metadata( bucket_name , '/tmp/php0IDtxE')
    #print(d.size)

    #return 
    #del_blob('sifinca-demo','/tmp/fondo.jpg')
    fd='/recycled-bin/'
    #mv_blob('sifinca-demo', '/tmp/php0Hi9Se','sifinca-demo',fd+'php0Hi9Se' )
    
   
    print(f'Cargando todos los blobs de {bucket_name}')
    blobs = get_list_blobs(bucket_name)
     #buscar blob en la base de datos 
   
    conn = get_conn()
    print(f'Cargando todos los path de la basedatos')
    files=get_allfiles(conn)
    n=0
    size=0
    nofound=[]
    for blob in blobs:
        n += 1 
        
        print(f'[{n}]Procesando blob {blob.name}')

        file = next((x for x in files if x[1] == blob.name), None)
         # Not found file - erase o move blob
        if file is None:
            print(f'{blob.name} no fue encontrado')
            nofound.append(blob.name)

            f= blob.name.split('/')  
            dest= fd+f[len(f)-1]              
            
            #mv_blob(bucket_name, blob.name,bucket_name,dest )
            print(f'{blob.name} fue movido a {dest}')
            size+=blob.size 
        else:
            print(f" --- > ID: {file[0]} / Path: {file[1]}")
        
        if n==1000:
            break

        
   
  
    t= size/(1024*1024)
    print(f"# archivos no encontrados: {len(nofound)}")
    print(f" Espacio salvado :{t} MB")
    print(f"=======================================")
    print(nofound)

 
if __name__=='__main__':
    main()

