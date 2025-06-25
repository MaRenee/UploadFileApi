from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from helper.data_transformer import DataTransformer
from repository.data_storage_repository import DataStorageRepository
from repository.file_storage_repository import FileStorageRepository
from helper.validation import file_validator



load_dotenv()

app = FastAPI()

fileStorageRepository = FileStorageRepository()
dataStorageRepository = DataStorageRepository()

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    try:
        file_validator.validate_file(file)
        contents = await file.read()
            
        fileStorageRepository.upload_blob(file.filename, contents)

        return {"filename": file.filename, "status": "Uploaded successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    
@app.post("/upload-file")
async def storage_uploadfile(file: UploadFile = File(...)):
    
    try:
        extension = file_validator.validate_file(file)
        contents = await file.read()
        
        fileStorageRepository.upload_blob(file.filename, contents)
        
        # download file from storage account
        downloaded_data = fileStorageRepository.download_blob(file.filename)
        
        # transform bytes from List of Objects (MyUser)
        users = DataTransformer.parse_data(downloaded_data, extension)

        for user in users:
            dataStorageRepository.add_user(user)
            
        return {
            "filename": file.filename,
            "status": "File uploaded, retrieved and read successfully!",
            "content": users
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Process failed: {str(e)}")
        