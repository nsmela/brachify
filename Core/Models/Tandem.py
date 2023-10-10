
class TandemModel:
    def __init__(self) -> None:
        self.name = ""
        self.shape = None # used to show the tandem
        self.shape_filepath = ""
        self.tool_shape = None # used to boolean cut from the final product
        self.tool_filepath = ""
        self.offsets = [0.0, 0.0, 0.0] # translate offsets 
        self.rotation = [0.0, 0, 0, 1] # rotation (0.0) on the positive z axis [0, 0, 1]
    
    def fromDict(self, data:dict) -> None:
        self.name = data
        self.offsets = data["Offsets"] # translate offsets 
        self.rotation = [0.0, 0, 0, 1] # rotation (0.0) on the positive z axis [0, 0, 1]
        
        # shapes

    def toDict(self) -> str:
        return {self.name: {
            "Display Model File": self.shape_filepath,
            "Tool Model File": self.tool_filepath, 
            "Offsets": self.offsets}}