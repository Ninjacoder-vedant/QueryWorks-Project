from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "725506272457-rpfvrq6jj1cgjih09oannfcau9m2gamu.apps.googleusercontent.com"
ALGORITHM = "HS256"

security = HTTPBearer()

def create_jwt(member_id: int):
    payload = {
        "member_id": member_id,
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security)
):
    token = creds.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["member_id"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")