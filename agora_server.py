import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.RtcTokenBuilder2 import *

def get_token(channel_name, uid):
    # Get the value of the environment variable AGORA_APP_ID. Make sure you set this variable to the App ID you obtained from Agora console.
    app_id = os.environ['app_id']
    # Get the value of the environment variable AGORA_APP_CERTIFICATE. Make sure you set this variable to the App certificate you obtained from Agora console
    app_certificate = os.environ['app_certificate']
    # Token validity time in seconds
    token_expiration_in_seconds = 3600
    # The validity time of all permissions in seconds
    privilege_expiration_in_seconds = 3600

    print("App Id: %s" % app_id)
    print("App Certificate: %s" % app_certificate)
    if not app_id or not app_certificate:
        print("Need to set environment variable AGORA_APP_ID and AGORA_APP_CERTIFICATE")
        return

    # Generate Token
    token = RtcTokenBuilder.build_token_with_uid(app_id, app_certificate, channel_name, uid, Role_Subscriber,
                                                 token_expiration_in_seconds, privilege_expiration_in_seconds)
    print("Token with int uid: {}".format(token))

    return {"rtcToken":token}
    
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PostRequest(BaseModel):
    uid: int
    channel: str

@app.post("/v1/fetchToken")
async def fetch_token(request: PostRequest):
    return get_token(request.channel, request.uid)

@app.get("/rtc/{channel_name}/publisher/uid/{uid}")
async def get_rtc_token(channel_name: str, uid: int):
    return get_token(channel_name, uid)

# To run the app:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("agora_server:app", reload=True, host="0.0.0.0", port=80)