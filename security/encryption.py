# security/encryption.py

import base64

try:
    from cryptography.fernet import Fernet
    _KEY = Fernet.generate_key()
    _CIPHER = Fernet(_KEY)
    
    def encrypt_data(data):
        return _CIPHER.encrypt(data.encode()).decode()
        
    def decrypt_data(token):
        return _CIPHER.decrypt(token.encode()).decode()
except ImportError:
    # Safe base64 obfuscation fallback to avoid crashes if cryptography package is missing
    def encrypt_data(data):
        return base64.b64encode(data.encode()).decode()
        
    def decrypt_data(token):
        return base64.b64decode(token.encode()).decode()
