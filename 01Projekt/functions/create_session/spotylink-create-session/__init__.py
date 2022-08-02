import logging
import uuid
import json
import string
import random

import azure.functions as func


def get_session_id() -> str:
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(8))


def get_session_persist(user_id, session_id):
    return {
        "partitionKey": "session",
        "session_id": session_id,
        "RowKey": user_id
    }


def main(req: func.HttpRequest, outputTable: func.Out[str]) -> func.HttpResponse:
    logging.info('Python Http trigger request to create a session')

    user_id = req.params.get('userid')

    session_id = req.params.get("sessionid")

    if not user_id:
        return func.HttpResponse(
             "The userid variable is missing in this request",
             status_code=400
        )

    if not session_id:      # If no session Id is set, create a new session
        session_id = get_session_id()

    logging.info(f'Spotylink session with id {session_id} created')
        
    data_json = get_session_persist(user_id=user_id, session_id=session_id)

    outputTable.set(json.dumps(data_json))

    logging.info(f"Session with Session-ID {session_id} created")

    return func.HttpResponse(
        json.dumps(data_json),
        status_code=200
    )

    
