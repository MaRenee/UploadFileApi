
from azure.storage.blob import BlobClient
import csv
import io


def download_blob_as_csv(connection_string: str, container_name: str, blob_name: str):
    try:
        
        blob = BlobClient.from_connection_string(
            conn_str=connection_string,
            container_name=container_name,
            blob_name=blob_name
        )

        blob_bytes = blob.download_blob().readall()

       
        blob_text = blob_bytes.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(blob_text))

        return list(csv_reader)

    except Exception as e:
        raise RuntimeError(f"Error reading CSV blob: {str(e)}")
