#!/usr/bin/env python3

import sys
from graph import graph
from logger import logger

state = {
    "notification_type": sys.argv[1],
    "host": sys.argv[2],
    "address": sys.argv[3],
    "service": sys.argv[4],
    "state": sys.argv[5],
    "output": sys.argv[6],
    "notification_mode": "initial",
}
logger.info("===== New Nagios Event =====")
logger.info(state)

graph.invoke(state)
logger.info("===== Investigation Finished =====")
