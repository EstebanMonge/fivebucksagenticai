from pathlib import Path
from logger import logger

PLAYBOOK_DIR = Path("/usr/local/nagios/playbooks")

def find_playbook(state):
    filename = f"{state['service']}.yml"
    playbook = PLAYBOOK_DIR / filename

    if playbook.exists():
        logger.info("Found playbook: %s", playbook)
        state["playbook"] = filename
        state["run_ansible"] = True
    else:
        logger.info("No playbook found for service '%s'", state["service"])
        state["playbook"] = None
        state["run_ansible"] = False

    return state

def playbook_router(state):
    if state["run_ansible"]:
        return "run_ansible_playbook"

    return "investigate"
