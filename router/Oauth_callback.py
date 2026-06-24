from fastapi import APIRouter, Request,Depends,status,HTTPException
from google_auth_oauthlib.flow import Flow
from fastapi.responses import RedirectResponse
from service.database import get_session
from service.database_schema import User_table
from service.jwt_token import create_access_token
from google.oauth2 import id_token
from sqlmodel import Session,select
from google.auth.transport import requests as google_requests
from dotenv import load_dotenv
import os
load_dotenv()
router = APIRouter(prefix="/api")
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

OAUTH_SECRET_FILE = os.getenv("OAUTH_SECRET_FILE", "/Users/shubham/Documents/Oauth_secret.json")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")


@router.get("/oauth/callback", tags=["User"])
def user_login(request: Request,db:Session=Depends(get_session)):
    try:
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        flow = Flow.from_client_secrets_file(
        OAUTH_SECRET_FILE,
        scopes=SCOPES
    )
        flow.redirect_uri = f"{BACKEND_URL}/api/oauth/callback"
        flow.fetch_token(
        authorization_response=str(request.url)
    )
        credentials = flow.credentials

        user_info = id_token.verify_oauth2_token(
        credentials.id_token,
        google_requests.Request(),
        os.getenv("CLIENT_ID"))
        Oauth_user={
        "email": user_info["email"],
        "name": user_info["name"],
        "google_id": user_info["sub"]
        }
        user=db.exec(select(User_table).where(User_table.email==Oauth_user["email"])).first()
        if user :
            payload={
            "id":user.id,
            "name":user.name,
            "email":user.email 
        }
            access_token=create_access_token(payload)
            print(access_token)
            return RedirectResponse(
    f"{FRONTEND_URL}/auth/callback?token={access_token}"
)
        else:
            new_user=User_table(
                name=Oauth_user["name"],
                email=Oauth_user["email"]
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            user=db.exec(select(User_table).where(User_table.email==Oauth_user["email"])).first()
            payload={
            "id":user.id,
            "name":user.name,
            "email":user.email 
        }
            access_token=create_access_token(payload)
            print(access_token)
            return RedirectResponse(
    f"{FRONTEND_URL}/auth/callback?token={access_token}"
)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))

