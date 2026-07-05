import json
import logging

logger = logging.getLogger(__name__)

def get_response_text_safely(response) -> str:
    """
    Safely extracts text from a GenerativeAI response, handling safety blocks and empty outputs.
    """
    try:
        if response and hasattr(response, "candidates") and response.candidates:
            if response.text:
                logger.debug("Successfully extracted text from response")
                return response.text.strip()
            logger.warning("Response has candidates but no text content")
        else:
            logger.warning("Response missing candidates or is empty")
    except Exception as e:
        logger.error(f"Error extracting response text: {e}")
    return ""

def parse_json_safely(json_str: str) -> dict:
    """
    Attempts to clean and parse a JSON string from the model.
    """
    if not json_str:
        logger.warning("Empty JSON string provided")
        return {}
    json_str = json_str.strip()
    if json_str.startswith("```json"):
        json_str = json_str[7:]
    if json_str.startswith("```"):
        json_str = json_str[3:]
    if json_str.endswith("```"):
        json_str = json_str[:-3]
    json_str = json_str.strip()
    
    try:
        result = json.loads(json_str)
        logger.debug("Successfully parsed JSON response")
        return result
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        return {}
