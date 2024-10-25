import json
import logging

logger = logging.getLogger(__name__)

def to_json(input, error_message="Failed to interpret JSON"):
    try:
        return json.loads(input)
    except Exception:
        raise Exception(f'{error_message}: "{input}"')

def try_parse_to_json(json_string: str):
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as error:
        logger.error(f"Error parsing json: {error}")
        return None
