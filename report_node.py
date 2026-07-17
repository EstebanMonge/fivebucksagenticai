import os
import requests
from dotenv import load_dotenv
from dokuwiki_node import create_dokuwiki_page


load_dotenv("/usr/local/nagios/agenticai/.env")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def report(state):

    message = f"""AI Investigation

Host: {state['host']}

Service: {state['service']}

{state['diagnosis']}
"""

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": message,
        },
        timeout=20,
    )

    #
    # Save the same content to DokuWiki
    #
    state["documentation"] = message

    create_dokuwiki_page(state)

    return state
