# api/stable_api.py

def api_response(success=True, data=None, error=None):
    return {
        "success": success,
        "data": data if success else None,
        "error": error if not success else None
    }
