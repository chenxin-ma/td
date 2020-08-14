import logging
from datetime import datetime


formatter = logging.Formatter('[%(levelname)s] %(message)s')



# logging.basicConfig(
#     level=logging.ERROR,
#     handlers=[
#         logging.FileHandler(root / "code/202008/logs/transactions.log", mode='w'),
#         # logging.StreamHandler()
#         ]
#     )


def setup_logger(name, log_file, level=logging.INFO, console=True):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file, mode='w') 
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    if console:
	    logger.addHandler(logging.StreamHandler())

    return logger



def getDaysInterval(str1, str2):

	date_format = "%Y-%m-%d"
	a = datetime.strptime(str1, date_format)
	b = datetime.strptime(str2, date_format)
	return (b - a).days
