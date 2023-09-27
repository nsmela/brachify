import numpy as np
import pydicom

class DicomData:
    def __init__(self):
        self.rs = None
        self.rp = None
        self.cylinder_origin = np.array([0, 0, 0])
        self.cylinder_base = np.array([0, 0, 0])
        self.cylinder_tip = np.array([0, 0, 0])
        self.cylinder_radius = 5.0
        self.needles = []
