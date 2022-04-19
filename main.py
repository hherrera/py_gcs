from webbrowser import get
from dotenv import load_dotenv
from services.gcs  import  get_list_blobs, del_blob
from db import  get_file

def main():
    # load .env
    load_dotenv()

    bucket_name ='sifinca-files'

    blobs = get_list_blobs(bucket_name)
    print(blobs.num_results)
    n=0
    nofound=[]
    for blob in blobs:
        n += 1 
        
        print(f'[{n}]Procesando registro {blob.name}')
        #buscar blob en la base de datos 
        s = blob.name.split("/")
        filename=s[len(s)-1]
        print(filename)
        file=get_file(filename)
        if not file:
            nofound.append(file)
            print(f'{blob.name} no encontrado')
        else:
            print(file)
        if n==1:
            break



        # Not found file - erase o move blob
    map(del_blob,nofound)
    print(nofound)






    


 
if __name__=='__main__':
    main()

