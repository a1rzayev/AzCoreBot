sessions = {}

def get_session(user_id):
    if user_id not in sessions:
        sessions[user_id] = {
            "state": "start",
            "lead_step": None,
            "lead_data": {}
        }
    return sessions[user_id]

def reset_session(user_id):
    sessions[user_id] = {
        "state": "start",
        "lead_step": None,
        "lead_data": {}
    }