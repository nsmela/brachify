
class Tandem:
    def __init__(self) -> None:
        self.shape = None
        self.offsets = [0.0, 0.0, 0.0] # translate offsets 
        self.rotation = [0.0, 0, 0, 1] # rotation on the positive z axis
        self.flipped = [1, 1, 1] # -1 means a flip in that direction