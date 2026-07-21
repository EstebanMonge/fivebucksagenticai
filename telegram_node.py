#!/usr/bin/env python3

import os
import requests
from dotenv import load_dotenv
from logger import logger

load_dotenv("/usr/local/nagios/agenticai/.env")

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send_telegram(state):
    mode = state.get("notification_mode", "initial")

    if mode == "remediation":
        message = f""" Automatic remediation

Host: {state["host"]}
Service: {state["service"]}

Playbook:
{state["playbook"]}

Status:
{state["ansible_status"]}

Output:
{state["ansible_output"]}
"""
    else:
        message = f"""Nagios Alert

Notification Type: {state.get("notification_type", "UNKNOWN")}

Host: {state["host"]}
Address: {state["address"]}

Service: {state["service"]}

State: {state["state"]}

Output:
{state["output"]}
"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        response = requests.post(
            url,
            json={
                "chat_id": CHAT_ID,
                "text": message,
                "disable_notification": True,
            },
            timeout=15,
        )

        logger.info("Telegram status code: %s", response.status_code)
        logger.info("Telegram response: %s", response.text)
        response.raise_for_status()
        logger.info("Initial Telegram notification sent successfully.")

    except Exception as e:
        logger.exception("Failed to send Telegram notification")

    return state
