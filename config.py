from pathlib import Path
from os import path
import os
from enum import Enum
from utils import *




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

loggerpath = root / "logs/transactions.log"
simLogPath = root / "logs/sim.log"
logger = setup_logger('1', loggerpath, console=False)
simLog = setup_logger('2', simLogPath, console=False)


MAX_INTEGER = 999999999
drawing = False

