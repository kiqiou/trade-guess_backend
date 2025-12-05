import hmac
import hashlib
import json

def verify_telegram_auth(data: dict, bot_token: str) -> bool:
    """
    Проверка подписи WebApp авторизации
    """
    check_hash = data.get("hash")
    if not check_hash:
        return False

    auth_data = data.copy()
    auth_data.pop("hash", None)

    sorted_data = "\n".join(f"{k}={auth_data[k]}" for k in sorted(auth_data.keys()))

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    h = hmac.new(secret_key, sorted_data.encode(), hashlib.sha256).hexdigest()

    return h == check_hash
