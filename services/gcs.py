from http import client
from google.cloud import storage
from google.cloud import exceptions
import json

class NotFoundError(Exception):
  """Raised when a resource is not found."""

# Error messages.
_GET_BLOB_ERROR_MSG = (
    'failed to retrieve Blob with name %r from Google Cloud Storage Bucket '
    '%r: %s')

def metadata_blob(bucket_name, object_name):
    try:
      client = storage.Client()
      bucket = client.bucket(bucket_name)
      blob =  blob = bucket.get_blob(object_name)
      
    except (AttributeError, exceptions.NotFound) as err:
      
      raise NotFoundError(_GET_BLOB_ERROR_MSG % (object_name, bucket_name, err))
    return blob


def list_blobs(bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    iterator = bucket.list_blobs()
   
    return iterator

def del_blob(bucket_name, object_name):
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
def mv_blob(bucket_name, blob_name, new_bucket_name, new_blob_name):
    """
    Function for moving files between directories or buckets. it will use GCP's copy 
    function then delete the blob from the old location.
    
    inputs
    -----
    bucket_name: name of bucket
    blob_name: str, name of file 
        ex. 'data/some_location/file_name'
    new_bucket_name: name of bucket (can be same as original if we're just moving around directories)
    new_blob_name: str, name of file in new directory in target bucket 
        ex. 'data/destination/file_name'
    """
    storage_client = storage.Client()
    source_bucket = storage_client.get_bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.get_bucket(new_bucket_name)

    # copy to new destination
    new_blob = source_bucket.copy_blob(
        source_blob, destination_bucket, new_blob_name)
    # delete in old destination
    source_blob.delete()
    
    print(f'File moved from {source_blob} to {new_blob_name}')

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob."""
 
    storage_client = storage.Client()
 
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
 
   
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the google storage bucket."""
 
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
 
    blob.upload_from_filename(source_file_name)
 
   

if __name__=='__main__':
    pass

