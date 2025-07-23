import unittest
import os
from repository.file_storage_repository import FileStorageRepository

class TestUploadFile(unittest.TestCase):

    def setUp(self):
        mode = "local"
        os.environ["ENV"] = mode
        os.environ["CONTAINER_NAME"] = "exemple"

        if mode == "local":
            os.environ["AZURE_STORAGE_CONNECTION_STRING"] = "DefaultEndpointsProtocol=https;AccountName=wemssoftwarestadv;AccountKey=fVJ3jKPEL7EN85Rvc70OMXnckNqMIqfV6ACDWNHbryRalH7krDfesawP8kWt5/Y4NfIv7F6GmrSF+AStvdjhcA==;EndpointSuffix=core.windows.net" 
        else:
            os.environ["ACCOUNT_URL"] = "https://wemssoftwarestadv.blob.core.windows.net"
        
    def test_upload_file(self):
        repo = FileStorageRepository()

        local_path = r"C:\Users\stell\Downloads\test.csv"
        blob_name = local_path 

        self.assertTrue(os.path.exists(local_path), f"Le fichier {local_path} n'existe pas")

        with open(local_path, "rb") as f:
            data = f.read()

        try:
            repo.upload_blob(blob_name, data)
        except Exception as e:
            self.fail(f"Échec de l'upload du fichier CSV : {e}")

        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()

