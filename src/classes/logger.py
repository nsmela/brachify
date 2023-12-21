import logging
import logging.handlers
import sys

from classes import info


# setup log formaters
template = '%(levelname)s %(module)s: %(message)s'
console_formatter = logging.Formatter(template)
file_formatter = logging.Formatter('%(asctime)s ' + template, datefmt='%H:%M:%S')
file_name = "app.log"

# Configure root logger for minimal logging
logging.basicConfig(level=logging.ERROR)

root_log = logging.getLogger()

log = root_log.getChild("Brachify")
log.setLevel(logging.DEBUG)
log.propagate = False

# rotating file handler
if not info.USER_PATH.exists():
    info.USER_PATH.mkdir(parents=True, exist_ok=True)

file_handler = logging.handlers.RotatingFileHandler(
    str(info.USER_PATH.joinpath(file_name)),
    encoding="utf-8",
    maxBytes=25*1024*1024,
    backupCount=3)

file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)
log.addHandler(file_handler)

# log to console as well
stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(console_formatter)
log.addHandler(stream_handler)
