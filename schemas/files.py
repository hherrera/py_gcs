
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Optional,Union

class FileOut(BaseModel):
    id: Union[str,UUID] 
    entrydate: datetime
    hash : Optional[str] = None
    path : str 
    originalname : str
    size : int 
    entity : Optional[str] = None
    entityid : Optional[str] = None
    ext : str
    mimetype : str
    bucket : str
    signed_url : str
    public_url : str

