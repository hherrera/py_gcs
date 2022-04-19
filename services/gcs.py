from http import client
from google.cloud import storage
def get_list_blobs(bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    iterator = bucket.list_blobs()
   
    return iterator

def delete(bucket_name, object_name):
        """
        Deletes an object from the bucket.

        :param bucket_name: name of the bucket, where the object resides
        :type bucket_name: str
        :param object_name: name of the object to delete
        :type object_name: str
        """
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name=object_name)
        blob.delete()

     