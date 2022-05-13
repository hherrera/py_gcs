import typer


from config.settings import settings
from commands import download, debug_blob

from config.handler_logging import logger



# manejador de comandos
app = typer.Typer()

# agregar comandos
app.add_typer(download.app, name="download")
app.add_typer(debug_blob.app, name="debug_files")

if __name__=='__main__':
    app()
    
    
