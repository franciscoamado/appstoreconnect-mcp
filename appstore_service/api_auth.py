import time
import jwt
from . import config

class AppStoreConnectAuth:
    def __init__(self):
        self.key_id = config.KEY_ID
        self.issuer_id = config.ISSUER_ID
        self.private_key_path = config.PRIVATE_KEY_PATH
        self.expiration_minutes = config.EXPIRATION_MINUTES
        self.base_url = "https://api.appstoreconnect.apple.com/v1"
        self._token = None
        self._token_generated_time = 0

    @property
    def token(self):
        # Check if token is expired or not generated
        if not self._token or (time.time() - self._token_generated_time) >= (self.expiration_minutes * 60):
            self._generate_jwt()
        return self._token

    def _generate_jwt(self):
        headers = {
            "alg": "ES256",
            "kid": self.key_id,
            "typ": "JWT"
        }
        now = int(time.time())
        payload = {
            "iss": self.issuer_id,
            "iat": now,
            "exp": now + (self.expiration_minutes * 60),
            "aud": "appstoreconnect-v1"
        }
        with open(self.private_key_path, "r") as key_file:
            private_key = key_file.read()

        self._token = jwt.encode(payload, private_key, algorithm="ES256", headers=headers)
        self._token_generated_time = now

    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        } 