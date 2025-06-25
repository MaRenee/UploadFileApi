import json
import csv
from io import StringIO
from typing import List

from fastapi import HTTPException
from model.ms_user import MsUser  

class DataTransformer:
    
    @staticmethod
    def parse_data(raw_data: bytes, extension: str) -> List[MsUser]:
        if extension == ".json":
            return DataTransformer.parse_json(raw_data)
        elif extension == ".csv":
            return DataTransformer.parse_csv(raw_data)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file extension.")
        
    @staticmethod
    def parse_json(raw_data: bytes) -> List[MsUser]:
        try:
            raw_content = raw_data.decode('utf-8')
            content = json.loads(raw_content)
            return [MsUser(**item) for item in content]
        except Exception as e:
            raise ValueError(f"Erreur de parsing JSON : {str(e)}")

    @staticmethod
    def parse_csv(raw_data: bytes) -> List[MsUser]:
        try:
            raw_content = raw_data.decode('utf-8')
            reader = csv.DictReader(StringIO(raw_content), delimiter=';')
            return [MsUser(**row) for row in reader]
        except Exception as e:
            raise ValueError(f"Erreur de parsing CSV : {str(e)}")
    

