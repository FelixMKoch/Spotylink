import json
import uuid
import logging
import base64
import requests

import azure.functions as func

SPOTIFY_USER_INFO_LINK = "https://api.spotify.com/v1/me"
SPOTIFY_AUTH_REDIRECT_LINK = "https://saveuser.azurewebsites.net/api/spotylink_auth?"
SPOTIFY_REQUEST_TOKEN_LINK = "https://accounts.spotify.com/api/token"

CLIENT_ID = "##################"
CLIENT_SECRET = "################"


def make_user_request(auth_token: str):

    auth_header = "Bearer " + auth_token

    ret = requests.get(SPOTIFY_USER_INFO_LINK, headers={"Authorization": auth_header})

    return ret


def get_auths(code):

    options= {
        "code": code,
        "redirect_uri": SPOTIFY_AUTH_REDIRECT_LINK,
        "grant_type": 'authorization_code'
    }

    res = requests.post(SPOTIFY_REQUEST_TOKEN_LINK, auth=(CLIENT_ID, CLIENT_SECRET), data = options)

    res_data = res.json()

    return res_data



def main(req: func.HttpRequest, outputTable: func.Out[str]) -> func.HttpResponse:
    logging.info('Python request to store User')

    code = req.params.get('code')

    state = req.params.get('state')

    res_dict = get_auths(code)

    logging.info(f"Authentication flow for user with ID {state} trriggered")

    if(res_dict.get('error')):
        return func.HttpResponse(
            "Einloggen hat nicht funktioniert.",
            status_code=400
        )

    back = make_user_request(res_dict["access_token"])

    if(back.status_code is not 200):
        return func.HttpResponse(
             "The auth variable was wrong.",
             status_code=400
        )

    data_json = {
        "partitionKey": "user",
        "auth_token": res_dict["access_token"],
        "refresh_token": res_dict["refresh_token"],
        "user_id": back.json()["id"],
        "display_name": back.json()["display_name"],
        "RowKey": state
    }

    outputTable.set(json.dumps(data_json))

    logging.info(f"Authentication flow for user with ID {state} completed. User created")

    return func.HttpResponse(
        "Go back to previous site",
        status_code=200
    )



    
