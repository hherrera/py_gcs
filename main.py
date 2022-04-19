from http import client
from google.cloud import storage
def get_list_blobs(bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    iterator = bucket.list_blobs()
   
    return iterator
    




def _get_blob_path(blob):
        """
        Gets blob path.
        :param blob: instance of :class:`google.cloud.storage.Blob`.
        :return: path string.
        """
        return blob.bucket.name + "/" + blob.name 

def delete(self, bucket_name, object_name):
        """
        Deletes an object from the bucket.

        :param bucket_name: name of the bucket, where the object resides
        :type bucket_name: str
        :param object_name: name of the object to delete
        :type object_name: str
        """
        client = self.get_conn()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name=object_name)
        blob.delete()

        self.log.info('Blob %s deleted.', object_name) 

def main():


    bucket_name ='sifinca-files'

    res = get_list_blobs(bucket_name)
   
    #for d in res:
     #   print(d.name)

    
    


   # bucket = client.get_bucket(bucket_name)




    #for blob in blobs:
     #   print(blob.name)


 
if __name__=='__main__':
    main()

