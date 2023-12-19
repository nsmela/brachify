from PySide6.QtCore import QObject, Signal

class AppSignals(QObject):
    """
    Defines signals available in the application

    Allows easy access by first getting the app with "app = get_app()" 
    and then referencing the signal in app.signals    
    """

    height_changed = Signal(float)  # height offset for cylinder
    exportFile = Signal(str)  # need to export the mesh
    viewChanged = Signal(int)  # set the page for the viewwidget