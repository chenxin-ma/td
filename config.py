from pathlib import Path
from os import path
from enum import Enum

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
	FULL = 2
