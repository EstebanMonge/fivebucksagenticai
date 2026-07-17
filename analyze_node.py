from llm import llm
from logger import logger

def analyze(state):
    prompt = f"""
You are a Senior Linux SRE.

A Nagios alert has occurred.

Host:
{state["host"]}

Address:
{state["address"]}

Service:
{state["service"]}

State:
{state["state"]}

Plugin Output:
{state["output"]}

Current Evidence:
{state["evidence"]}

Provide:

1. Probable root cause.
2. Confidence (0-100%).
3. Suggested investigation.
4. Suggested remediation.

Respond in markdown.
"""

    logger.info("Calling OpenRouter...")
    logger.info("Host: %s", state["host"])
    logger.info("Service: %s", state["service"])
    logger.info("Evidence: %s", state["evidence"])

    try:
        response = llm.invoke(prompt)

        logger.info("OpenRouter response received.")
        logger.info(response.content)

        state["diagnosis"] = response.content
        state["recommendation"] = response.content
        state["confidence"] = 0.90

    except Exception:
        logger.exception("OpenRouter request failed")
        raise

    return state
