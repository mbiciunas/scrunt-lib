import logging
from log_handler import LogHandler
from scripts.database import DataBase

_db = DataBase()

logger = logging.getLogger("MyLogger")
handler = LogHandler(_db, 123)
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

logger.debug("A DEBUG Message")
logger.info("An INFO")
logger.warning("A WARNING")
logger.error("An ERROR")
logger.critical("A message of CRITICAL severity")

try:
    x = 4
    y = 0
    print(x/y)
    logger.info(f"x/y successful with result: {x/y}.")
except ZeroDivisionError as err:
    logger.exception("Something went wrong...")

# scrunt = Scrunt(0)
# scrunt.log().info("This is a test")
