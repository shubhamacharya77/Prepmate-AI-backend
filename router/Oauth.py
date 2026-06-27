from fastapi import APIRouter,status,HTTPException
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv
import os
import logging
load_dotenv()

router = APIRouter(prefix="/api")

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]
@router.get("/oauth", tags=["User"])
def user_oauth():
    try:
        flow = Flow.from_client_config(
    {
        "web": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [
                f"https://prepmate-ai-backend-424301171233.asia-south1.run.app/api/oauth/callback"
            ],
        }
    },
    scopes=SCOPES,
)

        flow.redirect_uri = f"https://prepmate-ai-backend-424301171233.asia-south1.run.app/api/oauth/callback"

        authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        code_challenge=None
)

        return {
        "authorization_url": authorization_url
    }
    except Exception as e: 
        logging.error(f"OAuth initialization error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))