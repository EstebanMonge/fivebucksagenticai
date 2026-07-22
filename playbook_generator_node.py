import os
from pathlib import Path

from llm import llm
from logger import logger

PROPOSED_DIR = Path("/usr/local/nagios/playbooks/proposed")
PROPOSED_DIR.mkdir(parents=True, exist_ok=True)


def generate_playbook(state):

    filename = f"{state['service']}.yml"

    prompt = f"""
You are a Senior Linux SRE.

A Nagios service has no remediation playbook.

Generate ONLY a valid Ansible playbook.

Requirements:

- hosts: all
- gather_facts: false
- idempotent
- include descriptive task names
- use built-in Ansible modules whenever possible
- no markdown
- no explanation
- output only YAML

Service:
{state["service"]}

Host:
{state["host"]}

Address:
{state["address"]}

Nagios Output:
{state["output"]}

Evidence:
{state["evidence"]}

Diagnosis:
{state["diagnosis"]}
"""

    try:

        logger.info(
            "Generating playbook for service %s",
            state["service"]
        )

        response = llm.invoke(prompt)

        playbook = response.content.strip()

        path = PROPOSED_DIR / filename

        path.write_text(playbook)

        logger.info(
            "Playbook saved to %s",
            path
        )

        state["generated_playbook"] = str(path)

    except Exception as e:

        logger.exception("Unable to generate playbook")

        state["generated_playbook"] = None
        state["playbook_generation_error"] = str(e)

    return state
