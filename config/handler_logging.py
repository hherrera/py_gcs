import google.cloud.logging
from google.logging.type import log_severity_pb2 as severity
client = google.cloud.logging.Client()
client.setup_logging()
logger = client.logger(name="py_gcs")


