import re
from typing import Union


def decode_input_json(json: dict) -> Union[None, str]:
    """
    Decode JSON output of the route input.
    :param json: JSON of the input request.
    :return: Value of JSON or None in case of problems
    """
    if type(json) is dict:
        return json.get("input")
    return None


def value_is_ip_check(value: str) -> bool:
    """
    Verify if value match IP regex.
    :param value: Value to verify.
    :return: True if matched.
    """
    match = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", value)
    return bool(match)
