import logging
import logging.handlers

# setup log formaters
template = '%(levelname)s %(module)s: %(message)s'
console_formatter = logging.Formatter(template)
file_formatter = logging.Formatter('%(sctime)s ' + template, datefmt='%H:%M:%S')

# Configure root logger for minimal logging
logging.basicConfig(
    level=logging.DEBUG, 
    format=template)

log = logging.getLogger()

