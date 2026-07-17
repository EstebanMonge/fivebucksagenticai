#!/usr/bin/env python3

import os
import requests
from dotenv import load_dotenv
from logger import logger

load_dotenv("/usr/local/nagios/agenticai/.env")

DOKUWIKI_URL = os.environ["DOKUWIKI_URL"]
DOKUWIKI_API_TOKEN = os.environ["DOKUWIKI_API_TOKEN"]


def create_dokuwiki_page(state):

    page_id = (
        f"nagios:{state['host']}:"
        f"{state['service'].replace(' ', '_').lower()}"
    )


    content = f"""
====== AI Investigation ======

^ Field ^ Value ^
| Host | {state['host']} |
| Address | {state['address']} |
| Service | {state['service']} |
| State | {state['state']} |

===== Nagios Output =====

<code>
{state['output']}
</code>

===== AI Diagnosis =====

{state['diagnosis']}
"""

    payload = {
        "jsonrpc": "2.0",
        "id": "create-page",
        "method": "core.savePage",
        "params": {
            "page": page_id,
            "text": content,
            "summary": "Created by AgenticAI",
            "isminor": False,
        },
    }

    headers = {
        "Authorization": f"Bearer {DOKUWIKI_API_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            DOKUWIKI_URL,
            headers=headers,
            json=payload,
            timeout=15,
        )

        logger.info("Status code: %s", response.status_code)
        logger.info("Response: %s", response.text)

        response.raise_for_status()

        result = response.json()

        if result.get("error"):
            raise Exception(result["error"])

        logger.info("Page %s created successfully", page_id)

    except Exception:
        logger.exception("Failed to create Dokuwiki page")

    return state

def main():
    state = {
        "notification_type": "PROBLEM",
        "host": "odoocustomer",
        "address": "192.168.1.100",
        "service": "HTTP",
        "state": "CRITICAL",
        "output": "HTTP CRITICAL - 500 Internal Server Error",
    }

    result = create_dokuwiki_page(state)

    print("Done.")
    print(result)


if __name__ == "__main__":
    main()
