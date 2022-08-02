import logging
import json
import requests
import random

import azure.functions as func

SPOTIFY_TOP_TRACKS_LINK = "https://api.spotify.com/v1/me/top/tracks"


def create_playlist(auth: str, user_id: str, user_names):
    
    description = "Automated Playlist by Spotylink. Contributors to this playlist: "

    for user_name in user_names:
        description += user_name + " "

    auth_header = "Bearer " + auth
    ret = requests.post(
        f"https://api.spotify.com/v1/users/{user_id}/playlists", 
        headers={
			"Authorization": auth_header,
			"Content-Type": "application/json"
		},
        data=json.dumps({
            "name": "Spotylink Playlist",
            "description": description,
			"public": False
        })
        )
		
    logging.info(f"Created an empty playlist to Spotify account of user with ID {user_id}")

    return ret.json()


def get_top_items(auth: str):
    auth_header = "Bearer " + auth
    response = requests.get(
        SPOTIFY_TOP_TRACKS_LINK,
        headers={
            "Authorization": auth_header,
			"Content-Type": "application/json"
        }
    )

    res_json = response.json()

    res = []

    for i in range(20):
        try:
            res.append(res_json["items"][i]["uri"])
        except:
            pass

    return res



def post_to_playlist(auth, playlist_id, uris):

    auth_header = "Bearer " + auth

    ret = requests.post(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers={
            "Authorization": auth_header,
			"Content-Type": "application/json"
        },
        data=json.dumps({
            "uris": uris,
            "position": 0
        })
    )

    logging.info(f"Posted {len(uris)} songs to playlist with ID {playlist_id}")

    return ret


def get_top_30_shuffeled(top_list):
    res = list()

    for item in top_list:
        random.shuffle(item)
        if len(item) > 0:
            res.append(item[0])

    if len(res) >= 30:
        return res

    rest_list = []

    for item in top_list:
        if len(item) > 1:
            rest_list.extend(item[1:])

    random.shuffle(rest_list)

    for i in rest_list:
        if len(res) == 30:
            break
        
        res.append(i)

    return res


def main(req: func.HttpRequest, usersTable, sessionsTable) -> func.HttpResponse:
    logging.info('Python HTTP trigger Session Create Request')

    user_id = req.params.get('userid')
    spotify_user_id = ""

    user_list = json.loads(usersTable)
    session_list = json.loads(sessionsTable)
    playlist_create_return = ""
    user_auth = ""
    session_user_ids = []
    auths=[]
    track_uris = []
    user_names = []

    session_id = req.params.get('sessionid')

    if not user_id:
        return func.HttpResponse(
             "The user_id variable is missing in this request",
             status_code=400
        )
    
    if not session_id:
        return func.HttpResponse(
             "The sessionid variable is missing in this request",
             status_code=400
        )

    for session in session_list:
        if session["session_id"] == session_id:
            session_user_ids.append(session["RowKey"])
            

    for user in user_list:
        if user["RowKey"] == user_id:
            spotify_user_id = user["user_id"]
            user_auth = user["auth_token"]

        if user["RowKey"] in session_user_ids:
            auths.append(user["auth_token"])
            user_names.append(user["display_name"])

    playlist_create_return = create_playlist(user_auth, spotify_user_id, user_names)

    if playlist_create_return == "":
        return func.HttpResponse(
             f"Kein User mit der id {user_id} gefunden",
             status_code=400
        )

    
    for auth in auths:
        track_uris.append(get_top_items(auth))

    shuffeled_items = get_top_30_shuffeled(track_uris)

    # Export Playlist
    ret = post_to_playlist(user_auth, playlist_create_return["id"], shuffeled_items)

    logging.info(f"Export playlist to user with id {user_id} completed")

    return func.HttpResponse(
             str(ret),
             status_code=200
        )
