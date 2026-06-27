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
import logging
import os
load_dotenv()
router = APIRouter(prefix="/api")
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

@router.get("/oauth/callback", tags=["User"])
def user_login(request: Request,db:Session=Depends(get_session)):
    try:
        BACKEND_URL = os.getenv("BACKEND_URL", "https://prepmate-ai-backend-424301171233.asia-south1.run.app")
        FRONTEND_URL = os.getenv("FRONTEND_URL", "https://prepmate-ai-frontend.vercel.app")
        flow = Flow.from_client_config(
    {
        "web": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [
                f"{BACKEND_URL}/api/oauth/callback"
            ],    
        }
    },
    scopes=SCOPES,
)
        flow.redirect_uri = f"{BACKEND_URL}/api/oauth/callback"
        flow.fetch_token(
        authorization_response=str(request.url)
    )
        credentials = flow.credentials

        user_info = id_token.verify_oauth2_token(
        credentials.id_token,
        google_requests.Request(),
        os.getenv("GOOGLE_CLIENT_ID"))
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

            payload={
            "id":new_user.id,
            "name":new_user.name,
            "email":new_user.email 
        }
            access_token=create_access_token(payload)
            print(access_token)
            return RedirectResponse(
    f"{FRONTEND_URL}/auth/callback?token={access_token}"
)
    except Exception as e:
        logging.error(f"OAuth callback error: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(e))

