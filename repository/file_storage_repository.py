from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import os

class FileStorageRepository:
    def __init__(self):
        env = os.getenv("ENV")
        account_url = os.getenv("ACCOUNT_URL")
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")      
        self.container_name = os.getenv("CONTAINER_NAME")
         
        if not self.container_name:
            raise EnvironmentError("Missing CONTAINER_NAME environment variable")
        
        if env == "local":
            connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            if not connection_string:
                raise EnvironmentError("Missing AZURE_STORAGE_CONNECTION_STRING for local environment.")
            self.client = BlobServiceClient.from_connection_string(connection_string)

        else:
            credential = DefaultAzureCredential()
            self.client = BlobServiceClient(account_url=account_url, credential=credential)
        
    def upload_blob(self, filename: str, data: bytes) :
        try:
            blob_client = self.client.get_blob_client(container=self.container_name, blob=filename)
            blob_client.upload_blob(data, overwrite=True)
        except Exception as e:
            raise RuntimeError(f"Erreur lors de l'upload du blob : {str(e)}")

    def download_blob(self, filename: str) -> bytes:
        try:
            blob_client = self.client.get_blob_client(container=self.container_name, blob=filename)
            load = blob_client.download_blob()
            return load.readall()
        except Exception as e:
            raise RuntimeError(f"Erreur lors du téléchargement du blob : {str(e)}")
