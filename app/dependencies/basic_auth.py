import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from config import config

security = HTTPBasic()


def basic_auth(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    """
    Dummy function to simulate http basic auth.
    In reality, requests must go to authorization server if any, or to database
    :return: username if authorization is ok, else raise HTTPException(403)
    """
    username_check = secrets.compare_digest(config.DOCTOR_LOGIN, credentials.username)
    password_check = secrets.compare_digest(config.DOCTOR_PASSWORD, credentials.password)

    if not (username_check and password_check):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return credentials.username
