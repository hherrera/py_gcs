import datetime, time
import typer
from config.settings import settings
from services.gcs  import  list_blobs, mv_blob, del_blob
from services.db import  get_conn
from repositories.files import get_allfiles,

app=typer.Typer()

@app.command()
def delete_recycled():
    BUCKET_NAME='sifinca-backups'
    blobs= list_blobs(BUCKET_NAME,'recycled-bin')
    num=0
    for blob in blobs:
        del_blob(BUCKET_NAME,blob.name)
        num+=1
        typer.echo(f'{blob.name} fue eliminado')
    typer.echo(f'{num} blobs fueron eliminados ')

@app.command()
def purge_blobs(
    bucket_name : str= typer.Argument(..., help="Nombre del Bucket en Google Storage"),
    db_name : str ='sifincactg' , 
    bucket_name_dest : str = settings.BUCKET_NAME_DEST, 
    export : bool =True , 
    limit : int = 0 ,
    pretend : bool = True
    ):
    """
    Elimina los archivos de BUCKET_NAME, que no este en la base datos.

    Los archivos quedaran almacenados en el bucket 'sifinca-backups'  en la carpeta 'recycled-bin' .
    """
    basename = "notfound"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    export_file_name = "_".join([basename, suffix,'.txt']) # e.g. 'mylogfile_120508_171442'
   # int time
    inicio = time.time()
   
    nofound,n,size =debug_blob(db_name, bucket_name,bucket_name_dest ,settings.FOLDER_DEST,limit,pretend)
   
   # end time  
    fin = time.time() 
    duracion= fin - inicio
    typer.echo(f"=======================================")
    typer.echo(f"Tiempo en segundos: {duracion}")
    typer.echo(f"=======================================")
    typer.echo(f"Blobs recorridos en {bucket_name}: {n}")
    t= round(size/(1024*1024),0)
    typer.echo(f"# Enviados a {settings.FOLDER_DEST}: {len(nofound)}")
    typer.echo(f"Espacio recuperado :{t} MB")
    typer.echo(f"=======================================")
    # enviar archivo .csv
  
    if export:
        with open(export_file_name, 'w') as f:
            for l in nofound:
                f.write(l+'\n')


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
                print(f'{blob.name} fue movido a {bucket_name_dest}/{dest}')
            size+=blob.size 
        else:
            print(f" --- > Id: {file[0]} / Path: {file[1]}")
        if limit:
            if n==limit:
                break
    return nofound,n,size


if __name__=='__main__':
    app()