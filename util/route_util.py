import re
from typing import Union


def decode_input_json(json: dict) -> Union[None, str]:
    if type(json) is dict:
        return json.get("input")
    return None


def value_is_ip_check(value: str) -> bool:
    match = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", value)
    return bool(match)
