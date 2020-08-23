from pathlib import Path
from os import path
import os
from enum import Enum
from util.utils import *
import time
from tqdm import tqdm



root = Path("/Users/chenxinma/Documents/projects/td/")
datapath = root / 'data'

account_id = "425058922"
consumer_id = "QQTKS5USJAZU7MQLS9EEPQ8L4QVAMAGH"

with open(root / "token/access_token.txt", 'r') as file:
    access_token = file.read()
with open(root / "token/refresh_token.txt", 'r') as file:
    refresh_token = file.read()


class POSITION(Enum):
	EMPTY = 1
	PARTIAL = 2
	FULL = 3


class ERROR(Enum):
	NOT_ENOUGH_HISTORY = 1

loggerPath = root / "logs/logger.log"
transLogpath = root / "logs/transactions.log"
simLogPath = root / "logs/sim.log"
logger = setup_logger('logger', loggerPath, level=logging.INFO, console=True)
transLog = setup_logger('transLog', transLogpath, level=logging.INFO, console=False)
simLog = setup_logger('simLog', simLogPath, level=logging.INFO, console=False)


MAX_INTEGER = 999999999
drawing = False

