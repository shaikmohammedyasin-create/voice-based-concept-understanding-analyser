import time
import logging
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
from backend.utils.helpers import get_response_text_safely, parse_json_safely
from backend.ai.prompts import SYSTEM_PROMPT, build_user_prompt
from backend.models.response import EvaluationSchema

logger = logging.getLogger(__name__)

def configure_gemini(api_key: str):
    genai.configure(api_key=api_key)
    logger.info("Gemini API configured successfully")

def transcribe_audio(audio_bytes: bytes, mime_type: str) -> str:
    """
    Transcribes audio bytes utilizing Gemini 2.5 Flash with retry and timeout logic.
    """
    model = genai.GenerativeModel("gemini-2.5-flash")
    max_retries = 3
    delay = 2
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                [
                    {
                        "mime_type": mime_type,
                        "data": audio_bytes
                    },
                    "You are an expert audio transcriber. Transcribe the spoken words in this audio file word-for-word. Do not include filler word removal or edits. Provide only the plain text transcript, with no introductory text or feedback."
                ],
                request_options={"timeout": 90.0}
            )
            text = get_response_text_safely(response)
            if text:
                logger.info("Audio transcription successful")
                return text
        except GoogleAPIError as e:
            logger.error(f"Google API error during transcription (attempt {attempt + 1}): {e}")
            if attempt == max_retries - 1:
                raise e
            time.sleep(delay * (2 ** attempt))
        except Exception as e:
            logger.error(f"Unexpected error during transcription (attempt {attempt + 1}): {e}")
            if attempt == max_retries - 1:
                raise e
            time.sleep(delay * (2 ** attempt))
    return ""

def evaluate_explanation(concept_title: str, reference_description: str, keywords: list, transcript: str) -> dict:
    """
    Evaluates transcript conceptual similarity and keyword metrics with retry and timeout logic.
    """
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SYSTEM_PROMPT
    )
    user_prompt = build_user_prompt(concept_title, reference_description, keywords, transcript)
    max_retries = 3
    delay = 2
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                user_prompt,
                generation_config={
                    "response_mime_type": "application/json",
                    "response_schema": EvaluationSchema
                },
                request_options={"timeout": 90.0}
            )
            raw_text = get_response_text_safely(response)
            parsed = parse_json_safely(raw_text)
            if parsed:
                logger.info("Evaluation completed successfully")
                return parsed
        except GoogleAPIError as e:
            logger.error(f"Google API error during evaluation (attempt {attempt + 1}): {e}")
            if attempt == max_retries - 1:
                raise e
            time.sleep(delay * (2 ** attempt))
        except Exception as e:
            logger.error(f"Unexpected error during evaluation (attempt {attempt + 1}): {e}")
            if attempt == max_retries - 1:
                raise e
            time.sleep(delay * (2 ** attempt))
    return {}
