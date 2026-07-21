import os
from dotenv import load_dotenv
import ansible_runner
from logger import logger

load_dotenv("/usr/local/nagios/agenticai/.env")

ANSIBLE_DIR = os.getenv("ANSIBLE_DIR")
PLAYBOOK_DIR = os.getenv("ANSIBLE_PLAYBOOK_DIR")
ANSIBLE_CONFIG = os.getenv("ANSIBLE_CONFIG")
INVENTORY = os.getenv("ANSIBLE_INVENTORY")

os.environ["ANSIBLE_CONFIG"] = ANSIBLE_CONFIG

def run_ansible_playbook(state):
    playbook = os.path.join(
        PLAYBOOK_DIR,
        state["playbook"]
    )
    try:
        logger.info("Running playbook %s", playbook)
        logger.info("Inventory: %s", INVENTORY)
        logger.info("Limit: %s", state.get("host"))
        r = ansible_runner.run(
            private_data_dir=ANSIBLE_DIR,
            playbook=playbook,
            inventory=INVENTORY,
            limit=state.get("host"),
            extravars=state.get("extra_vars", {}),
        )
        output = []
        for event in r.events:
            stdout = event.get("stdout")
            if stdout:
                output.append(stdout)
        state["ansible_status"] = r.status
        state["ansible_rc"] = r.rc
        state["ansible_output"] = "\n".join(output)

    except Exception as e:
        logger.exception("Failed to execute Ansible playbook")

        state["ansible_status"] = "failed"
        state["ansible_rc"] = -1
        state["ansible_output"] = ""
        state["ansible_error"] = str(e)

    return state

def ansible_router(state):
    if state["ansible_rc"] == 0:
        state["notification_mode"] = "remediation"
        return "telegram"

    return "investigate"
