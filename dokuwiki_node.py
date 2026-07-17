#!/usr/bin/env python3

import os
import requests
from dotenv import load_dotenv
from logger import logger

load_dotenv("/usr/local/nagios/agenticai/.env")

DOKUWIKI_API_TOKEN = os.environ["DOKUWIKI_API_TOKEN"]


def create_dokuwiki_page(state):
    """
    LangGraph node that creates .
    """

    content = f"""Nagios Alert

Notification Type: {state.get("notification_type", "UNKNOWN")}

Host: {state["host"]}
Address: {state["address"]}

Service: {state["service"]}

State: {state["state"]}

Output:
{state["output"]}
}
"""

    url = "http://dokuwiki.sempaispacelab.lat/api/pages" 
    headers = {
        "Authorization": "Bearer YOUR_TOKEN",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(
            url,
            headers=headers,
            json={
                "id": "test",
                "content": content,
            },
            timeout=15,
        )

        logger.info("Dokuwiki status code: %s", response.status_code)
        logger.info("Dokuwiki response: %s", response.text)
        response.raise_for_status()
        logger.info("Dokuwiki page created successfully.")

    except Exception as e:
        logger.exception("Failed to create Dokuwiki page")

    return state
