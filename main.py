import random, string, time
from fastapi import FastAPI,Request
from config.handler_logging import logger, severity
##

from routes import files , blobs
# 
app=FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    request_path=request.url.path
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    json_msg = {
        "status_code":response.status_code,
        "request_id": idem,
        "time_process":formatted_process_time,
        "request_path":request_path
     
    }
    
    logger.log_struct(json_msg, severity.INFO)
    
    return response




@app.get('/')
async def home():
    return {"message":"OK"}

### incluir rutas
app.include_router(files.router, prefix='/api/files',tags=["files"])
app.include_router(blobs.router, prefix='/api/blobs',tags=['files'])


    # mapear respuesta

    
    
    
   
 
if __name__== '__main__':
    pass



