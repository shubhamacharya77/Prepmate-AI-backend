from fastapi import APIRouter,status,HTTPException
from google_auth_oauthlib.flow import Flow
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

@router.get("/oauth", tags=["User"])
def user_oauth():
    try:
        flow = Flow.from_client_secrets_file(
        OAUTH_SECRET_FILE,
        scopes=SCOPES
    )

        flow.redirect_uri = f"{BACKEND_URL}/api/oauth/callback"

        authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        code_challenge=None
)
        return {
        "authorization_url": authorization_url
    }
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))