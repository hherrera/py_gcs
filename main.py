import typer
import datetime
from typing import Optional
import time
from cli.debug_blob import debug_blob
from config.settings import settings
from cli.download import download_blob_id
# manejador de comandos
app = typer.Typer()

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

@app.command()
def download(id:str, destination_filename : Optional[str] = typer.Argument(None)):


    dest = download_blob_id(id,destination_filename)
    typer.echo(f'Archivo id {id} descargado en {dest}')


if __name__=='__main__':
   app()



