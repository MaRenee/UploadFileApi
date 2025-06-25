from azure.data.tables import TableServiceClient
from azure.identity import DefaultAzureCredential
import os

from model.ms_user import MsUser


class DataStorageRepository:
    def __init__(self):
        env = os.getenv("ENV")
        self.table_name = os.getenv("TABLE_NAME")
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        account_url = os.getenv("ACCOUNT_URL")
         
        if not self.table_name:
            raise EnvironmentError("Missing required environment variables: 'table_name'")
        
        if env == "local":
            if not connection_string:
                raise EnvironmentError("Missing AZURE_STORAGE_CONNECTION_STRING for local environment.")
            self.client = TableServiceClient.from_connection_string(connection_string)
            
        else:
            if not account_url:
                raise EnvironmentError("Missing TABLE_ACCOUNT_URL for cloud environment")
            self.service_client = TableServiceClient(endpoint=account_url, credential=DefaultAzureCredential())
        self.table_client = self.client.get_table_client(table_name=self.table_name)
        
    def add_user(self, user: MsUser):
        entity = user.to_entity()
        self.table_client.upsert_entity(entity)
                
            