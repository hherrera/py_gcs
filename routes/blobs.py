
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from services.db import get_conn
from repositories.files import get_file_id
from services.gcs import  download_blob
router = APIRouter()


@router.get("/{id}",response_class=FileResponse)
async def get_blob_id(id : str):
    conn = get_conn('sifincactg')
    bucket_name = 'sifinca-files'
    file = get_file_id(id,conn)
    if file is None:
        conn2 =  get_conn('sifincamtr')
        file = get_file_id(id,conn2)
        bucket_name = 'monteria-files'
        if file is None:
            # raise exception
            raise HTTPException(status_code=404,detail=f'Id:{id} not found')

    path = file['path']
    #blob = metadata_blob(bucket_name,path)
    file_path = 'static/'+str(file['id'])+'.'+file['ext']
    
    download_blob(bucket_name,path,file_path)

    
    return FileResponse(file_path)