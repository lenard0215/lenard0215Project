from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import oauth2
from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(prefix="/login", tags= ["Authentication"])

@router.post("/", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    
    if not utils.verify_pwd(user_credentials.password, user.password): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"invalid Credentials") 
    
    access_token = oauth2.create_acess_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}  