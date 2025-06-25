from pydantic import BaseModel, EmailStr, Field
from datetime import date
import uuid

class MsUser(BaseModel):
    lastname: str
    firstname: str
    date_of_birth: date 
    address: str
    postal_code: str
    city: str
    phone: str
    email: EmailStr
    partition_key: str = "default"
    row_key: str = Field(default_factory=lambda: str(uuid.uuid4()))

    def to_entity(self) -> dict:
        return {
            "PartitionKey": self.partition_key,
            "RowKey": self.row_key,
            "LastName": self.lastname,
            "FirstName": self.firstname,
            "DateOfBirth": self.date_of_birth.isoformat(), 
            "Address": self.address,
            "PostalCode": self.postal_code,
            "Phone": self.phone,
            "Email": self.email,
        }
