from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from Application.BRep.channel import generate_stacked_fused
from Presentation.MainWindow.core import MainWindow
from Presentation.MainWindow.display_functions import DisplayFunctions
from Core.Models.NeedleChannel import NeedleChannel

class NeedleFunctions(MainWindow):
    def setActiveNeedleChannel(self):
        pass
    def setNeedleRadiusAll(self):
        needles = []
        for needle in self.needles.channels:
            needles.append(NeedleChannel(
                number=needle.channelNumber, id=needle.channelID, points=needle.points, diameter=self.ui.channelRadiusSpinBox.value()))
        self.needles.channels = needles
        NeedleFunctions.__recalculate__(self)
        
    def setNeedleExtension(self):
        pass
    def setNeedleExteriorExtension(self):
        pass

    def __recalculate__(self):
        '''Called after the Needle Channels are changed'''
        self.display_needles_list = []
        self.display_needles = None
        for needle in self.needles.channels:
            shape = generate_stacked_fused(needle.points)
            self.display_needles_list.append(shape)
            if self.display_needles:
                self.display_needles = BRepAlgoAPI_Fuse(self.display_needles, shape).Shape()
            else:
                self.display_needles = shape
                
        DisplayFunctions.navigate_to_cylinder(self)