import functools

from PySide6.QtWidgets import QWidget

from classes.app import get_app
from classes.logger import log


def display_action(func):
    @functools.wraps(func)
    def wrapper_display_action(*args, **kwargs):
        try:
            func(*args, **kwargs)
        finally:
            displaymodel = get_app().window.displaymodel
            displaymodel.update()
        return None
    return wrapper_display_action


class CustomView(QWidget):    
    def on_close(self):
        log.debug("view closed")

    @display_action
    def on_open(self):
        log.debug("view open")

    def __init__(self):
        super().__init__()