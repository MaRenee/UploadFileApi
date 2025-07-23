import os
from dotenv import load_dotenv
import requests
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

# Azure AD Config
Tenant_ID = os.getenv("AZURE_TENANT_ID")
Client_ID = os.getenv("CLIENT_ID")  # Your API's App Registration client ID
AUTHORITY = f"https://login.microsoftonline.com/{Tenant_ID}"
ISSUER = f"{AUTHORITY}/v2.0"
JWKS_URL = f"{AUTHORITY}/discovery/v2.0/keys"

# Security scheme
security = HTTPBearer()

jwks_keys = requests.get(JWKS_URL).json()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        # Extract signing key ID from token header
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        # Find corresponding key in JWKS
        key = next((k for k in jwks_keys["keys"] if k["kid"] == kid), None)
        if not key:
            raise HTTPException(status_code=401, detail="Invalid token signature key")

        # Decode and verify token
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=Client_ID,
            issuer=ISSUER
        )

        return payload  

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation error: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
