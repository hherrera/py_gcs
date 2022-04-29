import json
import datetime
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
##
from services.db import get_conn
from repositories.files import get_file_id
from routes import files , blobs
# 
app=FastAPI()
@app.get('/')
async def home():
    return {"message":"OK"}

### incluir rutas
app.include_router(files.router, prefix='/api/files',tags=["files"])
app.include_router(blobs.router, prefix='/api/blobs',tags=['files'])


    # mapear respuesta

    
    
    
   
 
if __name__== '__main__':
    pass



