import json
import uuid
import logging
import base64
import requests

import azure.functions as func

SPOTIFY_USER_INFO_LINK = "https://api.spotify.com/v1/me"


def make_user_request(auth_token: str):

    auth_header = "Bearer " + auth_token

    ret = requests.get(SPOTIFY_USER_INFO_LINK, headers={"Authorization": auth_header})

    return ret.json()


def main(req: func.HttpRequest, usersTable) -> func.HttpResponse:
    logging.info('Python request to get user info')

    user_id = req.params.get("userid")

    user_list = json.loads(usersTable)

    if not user_id:
        return func.HttpResponse(
            "No userid given",
            status_code=400
        )

    token = ""

    for user in user_list:
        if user["RowKey"] == user_id:
            token = user["auth_token"]

    if(token == ""):
        return func.HttpResponse(
            "No User with the given ID found",
            status_code=400
        )

    logging.info(f"Fetching information for user with ID {user_id}")

    user_info = make_user_request(token)

    logging.info(f"Got information for user with ID {user_id}")

    return func.HttpResponse(
        json.dumps(user_info),
        status_code=200
    )



    
