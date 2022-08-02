from collections import UserList
import logging
import json

import azure.functions as func

def main(req: func.HttpRequest, sessionTable, userTable) -> func.HttpResponse:
    logging.info('Python Http trigger request to health check')
    session_json=json.loads(sessionTable)
    session_size=len(session_json)

    user_json=json.loads(userTable)
    user_size=len(user_json)
    
    result={
        "user_count": user_size,
        "session_count": session_size
    }
    
    return func.HttpResponse(
        json.dumps(result),
        status_code=200
    )

    
