# utils/error_handler.py

def safe_execute(func, default=None):
    try:
        return func()
    except Exception as e:
        return {
            "error": str(e),
            "fallback": default
        }
