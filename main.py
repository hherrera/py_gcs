from dotenv import load_dotenv
from services.gcs  import  get_list_blobs


def main():
    # load .env
    load_dotenv()

    bucket_name ='sifinca-files'

    blobs = get_list_blobs(bucket_name)
    print(blobs.num_results)
    n=0
    for blob in blobs:
        n += 1 
        
        print(f'Procesando registro {blob.name}')
        #buscar blob en la base de datos 
        
        # Not found file - erase o move blob






    


 
if __name__=='__main__':
    main()

