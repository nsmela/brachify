
class Tandem:
    def __init__(self) -> None:
        self.shape = None # used to show the tandem
        self.tool_shape = None # used to boolean cut from the final product
        self.offsets = [0.0, 0.0, 0.0] # translate offsets 
        self.rotation = [0.0, 0, 0, 1] # rotation (0.0) on the positive z axis [0, 0, 1]
        self.flipped = [1, 1, 1] # -1 means a flip in that XYZ direction