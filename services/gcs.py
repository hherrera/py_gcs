from http import client
from google.cloud import storage
from google.cloud import exceptions
import json
import datetime


class NotFoundError(Exception):
  """Raised when a resource is not found."""

# Error messages.
_GET_BLOB_ERROR_MSG = (
    'failed to retrieve Blob with name %r from Google Cloud Storage Bucket '
    '%r: %s')

def public_url(bucket, path):
    
    gcs_url = 'https://%(bucket)s.storage.googleapis.com/%(file)s' % {'bucket':bucket, 'file':path}
    return gcs_url

def signed_url(blob, hours : int=1):
    """Generates a v4 signed URL for downloading a blob.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """
    
    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(hours=hours),
        # Allow GET requests using this URL.
        method="GET",
    )

    return url

def metadata_blob(bucket_name, object_name):
    try:
      client = storage.Client()
      bucket = client.bucket(bucket_name)
      blob =  bucket.get_blob(object_name)
      
    except (AttributeError, exceptions.NotFound) as err:
      
      raise NotFoundError(_GET_BLOB_ERROR_MSG % (object_name, bucket_name, err))
    return blob



def list_blobs(bucket_name, prefix=None):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    if prefix is None:
        iterator = bucket.list_blobs()
    else:
        iterator = bucket.list_blobs(prefix=prefix)
   
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
 
def download_byte_range(
    bucket_name, source_blob_name, start_byte, end_byte, destination_file_name
):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # source_blob_name = "storage-object-name"

    # The starting byte at which to begin the download
    # start_byte = 0

    # The ending byte at which to end the download
    # end_byte = 20

    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name, start=start_byte, end=end_byte)

    print(
        "Downloaded bytes {} to {} of object {} from bucket {} to local file {}.".format(
            start_byte, end_byte, source_blob_name, bucket_name, destination_file_name
        )
    )


if __name__=='__main__':
    pass

