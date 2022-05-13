from turtle import pu
from fastapi import APIRouter,HTTPException
## local modules
from services.db import get_conn
from services.gcs import metadata_blob, signed_url, public_url
from repositories.files import get_file_id
from schemas.files import FileOut

## ruta
router = APIRouter()


@router.get('/{id}')
async def get_file_by_id(id:str):
    # buscar file las bases de datos
    conn = get_conn('sifincactg')
    bucket_name = 'sifinca-files'
    file = get_file_id(id,conn)
    if file is None:
        conn2 =  get_conn('sifincamtr')
        file = get_file_id(id,conn2)
        if file is None:
            # raise exception
            raise HTTPException(status_code=404,detail=f'Id:{id} not found')
        else:
             bucket_name = 'monteria-files'
    blob = metadata_blob(bucket_name,file['path'])
    url1 = signed_url(blob,48)
    url2 = public_url(bucket_name,file['path'])
    """
    result = FileOut(
        id=file['id'],
        entrydate = file['entrydate'], 
        hash= file['hash'], 
        path= file['path'],
        originalname= file['originalname'], 
        size= file['size'],
        entity= file['entity'],
        entityid= file['entityid'], 
        ext= file['ext'], 
        mimetype= file['mimetype'],
        bucket=bucket_name,signed_url=url1, public_url=url2
    )
    """
   
    file_dict = dict(file)
    result = FileOut(**file_dict, bucket=bucket_name,signed_url=url1, public_url=url2)

    return result
