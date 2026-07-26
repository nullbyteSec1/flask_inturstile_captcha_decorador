import httpx
from functools import wraps
from flask import request, jsonify


class FlaskTurnstile:
    def __init__(self, site_key: str, secret_key: str):
        self.site_key = site_key
        self.secret_key = secret_key

    def _verify(self) -> bool:
        token = request.form.get("cf-turnstile-response")

        if not token:
            return False

        remote_ip = request.headers.get(
            "CF-Connecting-IP",
            request.remote_addr
        )

        data = {
            "secret": self.secret_key,
            "response": token,
            "remoteip": remote_ip,
        }

        try:
            response = httpx.post(
                "https://challenges.cloudflare.com/turnstile/v0/siteverify",
                data=data,
                timeout=5,
            )

            response.raise_for_status()

            return response.json().get("success", False)

        except (httpx.HTTPError, ValueError):
            return False

    def required(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not self._verify():
                return jsonify(
                    {
                        "success": False,
                        "message": "Error verifying CAPTCHA; please try again"
                    }
                ), 403

            return func(*args, **kwargs)

        return wrapper
