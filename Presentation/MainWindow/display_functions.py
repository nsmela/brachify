# ref
# https://liuxinwin_admin.gitee.io/pythonocc-docs/OCC.Display.OCCViewer.html
#

from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import *
from OCC.Core.TopoDS import TopoDS_Shape


from Presentation.MainWindow.core import MainWindow

class DisplayFunctions(MainWindow):
    ## IMPORTS
    def navigate_to_imports(self):
        # variables

        # set page
        self.ui.stackedWidget.setCurrentIndex(0)
        
        # set display
        
        try:
            self.display._select_callbacks = []
            self.display.SetSelectionModeNeutral()
            
            self.display.EraseAll()

            # cylinder shown
            if self.brachyCylinder:
                shape = self.display_cylinder
                color = Quantity_Color(0.25, 0.25, 0.25, Quantity_TOC_RGB)
                self.display.DisplayColoredShape(shapes=shape, color=color)

        except Exception as error_message:
            print(error_message)

        try: 
            # needles shown
            if self.needles:
                color = Quantity_Color(0.35, 0.2, 0.35, Quantity_TOC_RGB)
                self.display.DisplayColoredShape(shapes=self.display_needles, color=color)

        except Exception as error_message:
            print(error_message)

        try: 
            # tandem
            if self.display_tandem:
                color = Quantity_Color(0.2, 0.55, 0.55, Quantity_TOC_RGB)
                self.display.DisplayColoredShape(shapes=self.display_tandem, color=color)

        except Exception as error_message:
            print(error_message)

        try:
            self.display.FitAll()
        except Exception as error_message:
            print(error_message)

    ## CYLINDER
    def navigate_to_cylinder(self):
        # variables

        # set page
        self.ui.stackedWidget.setCurrentIndex(1)
        
        # set display
        self.display._select_callbacks = []
        self.display.SetSelectionModeShape()
        
        try:
            self.display.EraseAll()

            # cylinder shown
            if self.brachyCylinder:
                shape = self.display_cylinder
                color = Quantity_Color(0.35, 0.2, 0.35, Quantity_TOC_RGB)
                self.display.DisplayColoredShape(shapes=shape, color=color)

        except Exception as error_message:
            print(f"ImportView: Cylinder load error: {error_message}")

        try: 
            # needles shown
            if self.needles:
                color = Quantity_Color(0.35, 0.2, 0.35, Quantity_TOC_RGB)
                self.display.DisplayShape(shapes=self.display_needles, material=Graphic3d_NOM_TRANSPARENT)

        except Exception as error_message:
            print(f"ImportView: Channels load error: {error_message}")

        try: 
            # tandem
            if self.display_tandem:
                color = Quantity_Color(0.2, 0.55, 0.55, Quantity_TOC_RGB)
                self.display.DisplayShape(shapes=self.display_tandem, material=Graphic3d_NOM_TRANSPARENT)

        except Exception as error_message:
            print(f"ImportView: Tandem load error: {error_message}")

        try:
            self.display.FitAll()
        except Exception as error_message:
            print(error_message)

    ## TANDEM
    def navigate_to_tandem(self):
        # variables

        # set page
        self.ui.stackedWidget.setCurrentIndex(3)
        
        # set display
        self.display._select_callbacks = []
        self.display.SetSelectionModeShape()
        
        try:
            self.display.EraseAll()

            # cylinder shown
            if self.brachyCylinder:
                shape = self.display_cylinder
                self.display.DisplayShape(shapes=shape, material=Graphic3d_NOM_TRANSPARENT)

        except Exception as error_message:
            print(error_message)

        try: 
            # needles shown
            if self.needles:
                self.display.DisplayShape(shapes=self.display_needles, material=Graphic3d_NOM_TRANSPARENT)

        except Exception as error_message:
            print(error_message)

        try: 
            # tandem
            if self.display_tandem:
                color = Quantity_Color(0.2, 0.2, 0.55, Quantity_TOC_RGB)
                self.display.DisplayColoredShape(shapes=self.display_tandem, color=color)

        except Exception as error_message:
            print(error_message)

        try:
            self.display.FitAll()
        except Exception as error_message:
            print(error_message)

    ## EXPORT
    def navigate_to_exports(self):
        # variables

        # set page
        self.ui.stackedWidget.setCurrentIndex(4)
        
        shape = None
        
        # set display
        self.display._select_callbacks = []
        self.display.SetSelectionModeNeutral()
        
        try:
            self.display.EraseAll()

            # cylinder shown
            if self.brachyCylinder:
                shape = self.display_cylinder

        except Exception as error_message:
            print(error_message)

        try: 
            # needles shown
            if self.needles:
                shape = BRepAlgoAPI_Cut(shape, self.display_needles).Shape()

        except Exception as error_message:
            print(error_message)

        try: 
            # tandem
            if self.tandem:
                shape = BRepAlgoAPI_Cut(shape, self.tandem.shape).Shape()

        except Exception as error_message:
            print(error_message)

        try:
            color = Quantity_Color(0.8, 0.1, 0.1, Quantity_TOC_RGB)
            self.display.DisplayShape(shapes=shape, color=color, material=Graphic3d_NOM_TRANSPARENT)
            self.display.FitAll()
            self.display_export = shape
        except Exception as error_message:
            print(error_message)
            
    def selectShape(self, shape, *kwargs) -> None:
        print(kwargs) # x and y of mouse click
        for s in shape:
            if s == self.display_cylinder:
                print("cylinder!")
            elif s == self.display_needles:
                print("needle group!")
            else:
                for i, needle in enumerate(self.display_needles_list):
                    if s == needle:
                        if i == self.needles_active_index:
                            self.needles_active_index = -1
                        else:
                            self.needles_active_index = i
                        print("needle single!")
                        DisplayFunctions.navigate_to_channels(self)
    
    def selectNeedle(self, shapes):
        index = -1
        if len(shapes) > 0:
            index  = needles.get_clicked_needle_index(self, shapes[0])
        self.needles_active_index = index
        DisplayFunctions.navigate_to_channels(self)