# security/access_control.py

ROLES = {
    "admin": ["read", "write", "delete"],
    "recruiter": ["read", "write"],
    "viewer": ["read"]
}

def has_access(role, action):
    return action in ROLES.get(role, [])
