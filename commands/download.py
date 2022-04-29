import typer
from typing import Optional
from repositories.files import get_file_id
from services.gcs import download_blob
from services.db import get_conn
app=typer.Typer()

@app.command()
def download(id:str, destination_filename : Optional[str] = typer.Argument(None)):


    # buscar db cartagena 
    conn1 = get_conn('sifincactg')
    file = get_file_id(id, conn1)
    
    if not file:
        conn2 = get_conn('sifincamon')
        file = get_file_id(id, conn2)
        if not file:
            # no encontrado error 
            typer.echo(f'ID no existe {id}')
        else:
            bucket_name ='monteria-files'
    # elseif monteria
    else:
        bucket_name = 'sifinca-files'        


    if  dest==None or dest=='':
        dest = file['originalname']
    path = file['path']
    typer.echo(bucket_name,file['path'])

    download_blob(bucket_name, path, dest)
    
    typer.echo(f'Archivo id {id} descargado en {dest}')


if __name__=='__main__':
    app()
    