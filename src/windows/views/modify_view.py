from PySide6.QtWidgets import QWidget

from classes.app import get_app
from classes.logger import log
from windows.models.shapemodel import ShapeModel
from windows.ui.modify_mesh_view_ui import Ui_Modify_View


class Modify_View(QWidget):

    def actionAddSphere(self):
        from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
        from OCC.Core.gp import gp_Pnt
        from random import randint

        amount = 10

        log.info(f"Adding {amount} spheres to the viewer for testing")
        label = "test_sphere"
        shapes = []
        for i in range(amount):
            point = gp_Pnt(randint(-30, 30), randint(-30, 30), 0)
            shape = BRepPrimAPI_MakeSphere(point, randint(5, 10)).Shape()
            shape_model = ShapeModel(
                label=f"{label}_{i}", shape=shape, rgb=(0.1, randint(0, 10) / 10, 0.9))
            shapes.append(shape_model)

        app = get_app()
        app.window.displaymodel.add_shapes(shapes)

    def actionRemoveSphere(self):
        from random import randint
        app = get_app()

        shapes = list(app.window.displaymodel.shapes.values())
        if len(shapes) < 1:
            return

        label = shapes[randint(0, len(shapes) - 1)].label

        app.window.displaymodel.remove_shape(label)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Modify_View()
        self.ui.setupUi(self)

        # signals and slots
        self.ui.btn_add_sphere.pressed.connect(self.actionAddSphere)
        self.ui.btn_remove_sphere.pressed.connect(self.actionRemoveSphere)
