import os
from fastapi import HTTPException, UploadFile, File

class file_validator:
    ALLOWED_TYPES = {"text/csv": ".csv", "application/json": ".json"}
    
    @classmethod
    def validate_file(cls, file: UploadFile) -> str:
        content_type = file.content_type
        
        if file.content_type not in cls.ALLOWED_TYPES:
            raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type: {file.content_type}. Only CSV and JSON files are allowed."
        )
        expected_extension = cls.ALLOWED_TYPES[content_type]      
        shortname, extension = os.path.splitext(file.filename)
    

        if extension.lower() != expected_extension:
            raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension '{extension}'. Expected '{expected_extension}' for content type '{file.content_type}'."
        )
        return expected_extension