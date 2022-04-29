from fastapi import APIRouter,HTTPException
## local modules
from services.db import get_conn
from repositories.files import get_file_id
from schemas.files import FileOut

## ruta
router = APIRouter()


@router.get('/{id}')
async def get_file_by_id(id:str):
    # buscar file las bases de datos
    conn = get_conn('sifincactg')
    
    file = get_file_id(id,conn)
    if file is None:
        conn2 =  get_conn('sifincamtr')
        file = get_file_id(id,conn2)
        if file is None:
            # raise exception
            raise HTTPException(status_code=404,detail=f'Id:{id} not found')
   
    
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
        mimetype= file['mimetype']
    )
    """
    file_dict = dict(file)
    result = FileOut(**file_dict)

    return result
