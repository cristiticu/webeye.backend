import base64
from datetime import datetime
import json


def parse_user_agent(user_agent: str):
    formatted_user_agent = user_agent.lower()

    browser = "Unknown"
    if "chrome" in formatted_user_agent and "edg" not in formatted_user_agent:
        browser = "Chrome"
    elif "firefox" in formatted_user_agent:
        browser = "Firefox"
    elif "safari" in formatted_user_agent and "chrome" not in formatted_user_agent:
        browser = "Safari"
    elif "edg" in formatted_user_agent:
        browser = "Edge"
    elif "opera" in formatted_user_agent or "opr" in formatted_user_agent:
        browser = "Opera"

    return browser


def format_utc_datetime_string(utc_datetime: datetime):
    return utc_datetime.isoformat().replace("+00:00", "Z")


def encode_last_evaluated_key(key):
    json_str = json.dumps(key)
    base64_str = base64.urlsafe_b64encode(json_str.encode()).decode()

    return base64_str


def decode_last_evaluated_key(base64_key: str):
    json_str = base64.urlsafe_b64decode(s=base64_key.encode()).decode()
    key = json.loads(json_str)

    return key
