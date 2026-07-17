import logging
import os

LOG_DIR = "/usr/local/nagios/var"
LOG_FILE = os.path.join(LOG_DIR, "agenticai.log")

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("agenticai")

if not logger.handlers:
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
