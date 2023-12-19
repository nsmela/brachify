from classes.app import get_app
from classes.logger import log
from windows.views.channels_view import ChannelsView
from windows.views.cylinder_view import CylinderView
from windows.views.export_view import Export_View
from windows.views.import_view import ImportView
from windows.views.tandem_view import TandemView


class NavigationModel():

    def __init__(self):
        log.debug(f"Navigation model initializing!")
        self.current_page = 0
        self.views = []
        self.views.append(ImportView())
        self.views.append(CylinderView())
        self.views.append(ChannelsView())
        self.views.append(TandemView())
        self.views.append(Export_View())

        # adding views to the main window from the self.views list
        app = get_app()
        window = app.window
        for i, view in enumerate(self.views):
            window.ui.viewswidget.widget(i).layout().addWidget(view)

        # signals
        app.signals.viewChanged.connect(self.set_page)

        # initializing the first page
        self.views[0].on_open()
        get_app().window.ui.viewswidget.setCurrentIndex(0)

        log.debug(f"Navigation model initialized")

    def set_page(self, page:int):
        if page == self.current_page: return
        log.debug(f"setting page to {page}")
        self.views[self.current_page].on_close()
        self.current_page = page
        self.views[self.current_page].on_open()
        get_app().window.ui.viewswidget.setCurrentIndex(page)