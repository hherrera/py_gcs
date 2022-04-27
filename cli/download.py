from services.db import get_conn, get_file_by_id
from services.gcs import download_blob


def download_blob_id(id:str, dest :str =None):

    # buscar db cartagena 
    conn1 = get_conn('sifincactg')
    file = get_file_by_id(id, conn1)
    
    if not file:
        conn2 = get_conn('sifincamon')
        file = get_file_by_id(id, conn2)
        if not file:
            # no encontrado error 
            print(f'ID no existe {id}')
        else:
            bucket_name ='monteria-files'
    # elseif monteria
    else:
        bucket_name = 'sifinca-files'        


    if  dest==None or dest=='':
        dest = file['originalname']
    path = file['path']
    print(bucket_name,file['path'])

    download_blob(bucket_name, path, dest)
    
    return dest


if __name__=='__main__':
    pass
    download('ac79f947-133b-4e92-afd9-3914a343dfbe')
    download('e6e81268-a058-40a6-abf1-3d3a1260f5b9')
