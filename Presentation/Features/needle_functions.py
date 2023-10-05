from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.TopoDS import TopoDS_Shape
from PyQt5.QtWidgets import QListWidgetItem
from Application.BRep.channel import generate_curved_channel
from Presentation.MainWindow.core import MainWindow
from Presentation.MainWindow.display_functions import DisplayFunctions
from Core.Models.NeedleChannel import NeedleChannel

class NeedleFunctions(MainWindow):
    '''
    Manages the functions and display values for the Needles and the Channel View
    self.display_needles: all needle channels fused as a single model
    self.display_needle_list: a list of the needle channels
    self.needles_active_index: the current active needle channel
    '''

    def setActiveNeedleChannel(self, index:int = -1) -> None:
        self.needles_active_index = index
        if len(self.ui.channelsListWidget.selectedIndexes()) < 1 or \
            index != self.ui.channelsListWidget.selectedIndexes()[0].row():
            self.ui.channelsListWidget.setCurrentRow(index)
        DisplayFunctions.navigate_to_channels(self)
    
    def setCylinderVisibility(self) -> None:
        self.isCylinderHidden = self.ui.checkBox_hide_cylinder.isChecked()
        DisplayFunctions.navigate_to_channels(self)

    def get_clicked_needle_index(self, shape) -> int:
        for i, needle in enumerate(self.display_needles_list):
            if shape == needle:
                return i

        return -1
    
    def setChannelOffset(self, offset:int) -> None:
        index = self.needles_active_index
        if index < 0:
            return
        
        old_value = self.ui.slider_needle_extension.value()
        if old_value != offset:
            self.ui.slider_needle_extension.setValue(offset)
            
        channel = self.needles.channels[self.needles_active_index]
        channel.curve_downwards = offset
        for channel in self.needles.channels:
            print(channel.toString())
        
        NeedleFunctions.recalculate(self)

    def setNeedleDisabled(self):
        index = self.needles_active_index
        if index < 0:
            return
        
        channel = self.needles.channels[self.needles_active_index]
        channel.disabled = not channel.disabled
        NeedleFunctions.recalculate(self)

    def recalculate(self):
        '''
        Called after the Needle Channels are changed.
        Generates each channel's shape and saves them in self.display_needles_list
        Then fuses them together and saves that model in self.display_needles
        
        the needles list is used only for channels view
        the fused model is used in all other views and to boolean subtract
        '''
        diameter = self.ui.channelDiameterSpinBox.value()
        self.display_needles_list = []
        self.display_needles = None
        for needle in self.needles.channels:
            if needle.disabled:
                continue
            shape = generate_curved_channel(
                channel=needle, 
                cylinder_offset= self.ui.cylinderLengthSpinBox.value() - 200.0,
                diameter=self.ui.channelDiameterSpinBox.value())
            self.display_needles_list.append(shape)
            if self.display_needles:
                self.display_needles = BRepAlgoAPI_Fuse(self.display_needles, shape).Shape()
            else:
                self.display_needles = shape
                
        DisplayFunctions.navigate_to_channels(self)