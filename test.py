from  fastapi import FastAPI

app = FastAPI()

@app.get('/{name}')
def home(name:str):
    return {"messase":f'Hola {name}'}

@app.get('/goodbye/{name}')
def good_bye(name:str):
    """Se despide de NAME """
    return {"messase":f'Chao {name}'}



if __name__=='__main__':
    app()
