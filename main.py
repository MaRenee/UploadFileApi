from fastapi import FastAPI, UploadFile, File
from azure.storage.blob import BlobServiceClient

app = FastAPI()

Azure_connection_string = "DefaultEndpointsProtocol=https;AccountName=wemssoftwarestadv;AccountKey=fVJ3jKPEL7EN85Rvc70OMXnckNqMIqfV6ACDWNHbryRalH7krDfesawP8kWt5/Y4NfIv7F6GmrSF+AStvdjhcA==;EndpointSuffix=core.windows.net"
container_name = "exemple"

blob_service_client = BlobServiceClient.from_connection_string(Azure_connection_string)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Upload file to Azure Blob Storage
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)
        contents = await file.read()
        blob_client.upload_blob(contents, overwrite=True)

        return {"filename": file.filename, "status": "Uploaded successfully!"}
    except Exception as e:
        return {"error": str(e)}