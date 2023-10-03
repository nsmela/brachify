from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from PyQt5.QtWidgets import QListWidgetItem
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

    def setActiveNeedleIndex(self):
        index = self.ui.channelsListView.selectedIndexes()[0].row()
        self.needles_active_index = index
        NeedleFunctions.__recalculate__(self)

    def selectChannel(shape, *kwargs):
        
        print(shape)
        
    def channelSelected(item: QListWidgetItem):
        print("Needle selected in needle channel list view!")
        print(item.text())
        print("Row: " + item.row())
        
    def channelSelectionChanged(self):
        index = self.ui.channelsListWidget.selectedIndexes()[0].row()
        label = self.ui.channelsListWidget.selectedItems()[0].text()
        print(label + ": " + str(index))
        self.needles_active_index = index 
        DisplayFunctions.navigate_to_channels(self)
        
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
                
        DisplayFunctions.navigate_to_channels(self)