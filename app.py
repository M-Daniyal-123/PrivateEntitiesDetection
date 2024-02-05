import os
import datetime
from typing import Dict

import http

from schema import PrivacyText
from config import app, pipe
from utils import post_process_ner, logging


@app.get("/")
def healthcheck() -> Dict:
    """
    End Point to check the health of svc

    Returns:
        Dict: health check status
    """
    response = {
        "status": http.HTTPStatus.OK,
        "message": "NER API is up and working",
        "meta": {},
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    return response


@app.post("/entities/extract")
async def extract_entities(input_text: PrivacyText) -> Dict:
    """
    Given an input text (str) or list of text, it extract the privacy entities

    Args:
        input_text (PrivacyText): Text (Str) or List (Str)

    Returns:
        Dict: return the response in dict with the entites in the text
    """
    try:
        logging.info("Running the pipeline")
        # Get the Entities from the NER Model
        raw_entities = pipe(input_text.text)

        logging.debug("Do some post processing on the entities")
        # Some Post Processing
        if isinstance(input_text.text, list):
            processed_entites = post_process_ner(raw_entities=raw_entities, islist=True)
        else:
            processed_entites = post_process_ner(
                raw_entities=raw_entities, islist=False
            )

    except Exception as e:

        logging.error(f"There's an exception in extract entities api {e}")
        response = {
            "status": http.HTTPStatus.BAD_REQUEST,
            "message": "There's an Error, Please checkout the logs",
            "meta": {},
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "entities": [],
        }

        return response

    # Todo: Store the data in a database
    # .......

    logging.info("Returning the entities")
    response = {
        "status": http.HTTPStatus.OK,
        "message": "The Privacy entities",
        "meta": {},
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "entities": processed_entites,
    }

    return response
