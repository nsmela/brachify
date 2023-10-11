from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.TopoDS import TopoDS_Shape
from PyQt5.QtWidgets import QListWidgetItem
from Application.BRep.channel import generate_curved_channel
from Presentation.MainWindow.core import MainWindow
import Presentation.Features.NeedleChannels.NeedlesDisplay as needlesDisplay
from Core.Models.NeedleChannel import NeedleChannel

'''
Manages the functions and display values for the Needles and the Channel View
self.display_needles: all needle channels fused as a single model
self.display_needle_list: a list of the needle channels
self.needles_active_index: the current active needle channel
'''

def setActiveNeedleChannel(window: MainWindow, index:int = -1) -> None:
    window.needles_active_index = index
    if len(window.ui.channelsListWidget.selectedIndexes()) < 1 or \
        index != window.ui.channelsListWidget.selectedIndexes()[0].row():
        window.ui.channelsListWidget.setCurrentRow(index)
    needlesDisplay.view(window)
    
def setCylinderVisibility(window: MainWindow) -> None:
    window.isCylinderHidden = window.ui.checkBox_hide_cylinder.isChecked()
    needlesDisplay.view(window)

def get_clicked_needle_index(window: MainWindow, shape) -> int:
    for i, needle in enumerate(window.display_needles_list):
        if shape == needle:
            return i

    return -1
    
def setChannelOffset(window: MainWindow, offset:int) -> None:
    index = window.needles_active_index
    if index < 0:
        return
        
    old_value = window.ui.slider_needle_extension.value()
    if old_value != offset:
        window.ui.slider_needle_extension.setValue(offset)
            
    channel = window.needles.channels[window.needles_active_index]
    channel.curve_downwards = offset
        
    reshape(window, channel)

def setNeedleDisabled(window: MainWindow):
    index = window.needles_active_index
    if index < 0:
        return
        
    channel = window.needles.channels[window.needles_active_index]
    channel.disabled = not channel.disabled
    recalculate(window)

def recalculate(window: MainWindow):
    '''
    Called after the Needle Channels are changed.
    Generates each channel's shape and saves them in self.display_needles_list
    Then fuses them together and saves that model in self.display_needles
        
    the needles list is used only for channels view
    the fused model is used in all other views and to boolean subtract
    
    also set the tandem offset from the first needle channel
    '''
    print("Recalculating channels!")
    diameter = window.ui.channelDiameterSpinBox.value()
    window.display_needles_list = []
    window.display_needles = None
    for needle in window.needles.channels:
        if needle.disabled:
            continue
        needle.shape = generate_curved_channel(
            channel=needle, 
            cylinder_offset= window.ui.cylinderLengthSpinBox.value() - 200.0,
            diameter=window.ui.channelDiameterSpinBox.value())
        window.display_needles_list.append(needle.shape)
        if window.display_needles:
            window.display_needles = BRepAlgoAPI_Fuse(window.display_needles, needle.shape).Shape()
        else:
            window.display_needles = needle.shape
    
    set_tandem_offsets(window)
    needlesDisplay.view(window)
    
def reshape(window: MainWindow, channel: NeedleChannel):
    '''
    Needle Channel shapes are saved within the NeedleChannel class
    '''
    
    print("reshaping channels")
    diameter = window.ui.channelDiameterSpinBox.value()
    cylinder_offset= window.ui.cylinderLengthSpinBox.value() - 200.0
    window.display_needles = None # can be recalulated later when needed
    if channel.disabled:
        channel.shape = None
    else:
        channel.shape = generate_curved_channel(channel=channel, cylinder_offset=cylinder_offset, diameter=diameter)

    set_tandem_offsets(window)
    needlesDisplay.update(window)
    

def set_tandem_offsets(window: MainWindow) -> None:
    tandem_channel = window.needles.channels[0]
    
    # position
    window.tandem_offset_position = tandem_channel.points[0]
    
    # rotation
    window.tandem_offset_rotation = 0.0 # TODO