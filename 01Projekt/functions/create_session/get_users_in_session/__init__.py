from collections import UserList
import logging
import json

import azure.functions as func

def main(req: func.HttpRequest, sessionTable, userTable) -> func.HttpResponse:
    logging.info('Python Http trigger request to get users in session')

    session_id = req.params.get("sessionid")

    if not session_id:
        return func.HttpResponse(
            "No sessionid found",
            status_code=400
        )   

    session_list = json.loads(sessionTable)

    user_list = json.loads(userTable)

    usersids = []
    usernames = []
    userdict = {}

    for user in user_list:
        userdict[user["RowKey"]] = user["display_name"]

    for session in session_list:
        if session["session_id"] == session_id:
            usersids.append(session["RowKey"])

    for userid in usersids:
        usernames.append(userdict[userid])

    user_count = str(len(usernames))

    logging.info(f"Found {user_count} user in session with ID {session_id}")

    return func.HttpResponse(
        json.dumps(usernames),
        status_code=200
    )

    
