from dotenv import load_dotenv
from fastapi import Depends, FastAPI, UploadFile, File, HTTPException
from helper.authentication import verify_token
from helper.data_transformer import DataTransformer
from repository.data_storage_repository import DataStorageRepository
from repository.file_storage_repository import FileStorageRepository
from helper.validation import file_validator
from repository.download_data_repository import download_blob_as_csv
from fastapi.responses import JSONResponse

import os




load_dotenv()

app = FastAPI()

fileStorageRepository = FileStorageRepository()
dataStorageRepository = DataStorageRepository()

AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
BLOB_NAME = "emp1.csv"  

@app.get("/download-file", response_class=JSONResponse)
def download_file():
    try:
        data = download_blob_as_csv(
            connection_string=AZURE_CONNECTION_STRING,
            container_name=CONTAINER_NAME,
            blob_name=BLOB_NAME
        )
        return JSONResponse(content=data)

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), user: dict = Depends(verify_token)):

    try:
        file_validator.validate_file(file)
        contents = await file.read()
            
        fileStorageRepository.upload_blob(file.filename, contents)

        return {"filename": file.filename, "status": "Uploaded successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    
@app.post("/upload-file")
async def storage_uploadfile(file: UploadFile = File(...), user: dict = Depends(verify_token)):
    
    try:
        extension = file_validator.validate_file(file)
        contents = await file.read()
        
        fileStorageRepository.upload_blob(file.filename, contents)
        
        # download file from storage account
        downloaded_data = fileStorageRepository.download_blob(file.filename)
        
        # transform bytes from List of Objects (MyUser)
        users = DataTransformer.parse_data(downloaded_data, extension)

        for u in users:
            dataStorageRepository.add_user(u)
            
        return {
            "filename": file.filename,
            "status": "File uploaded, retrieved and read successfully!",
            "content": users
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Process failed: {str(e)}")
        
        