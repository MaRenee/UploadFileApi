from fastapi import FastAPI, UploadFile, File, HTTPException
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os 


# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Read config from environment variables
Azure_connection_string = os.getenv("Azure_connection_string")
container_name = os.getenv("container_name")

blob_service_client = BlobServiceClient.from_connection_string(Azure_connection_string)

# Allowed content types
ALLOWED_TYPES = {"text/csv": ".csv", "application/json": ".json"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    
    # Validate file type

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type: {file.content_type}. Only CSV and JSON files are allowed."
        )
        
    # Extract and validate file extension
    shortname, extension = os.path.splitext(file.filename)
    expected_extension = ALLOWED_TYPES[file.content_type]

    if extension.lower() != expected_extension:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension '{extension}'. Expected '{expected_extension}' for content type '{file.content_type}'."
        )

    try:
        contents = await file.read()
            
        # Upload file to Azure Blob Storage
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)
        blob_client.upload_blob(contents, overwrite=True)

        return {"filename": file.filename, "status": "Uploaded successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")