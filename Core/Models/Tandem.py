
class TandemModel:
    def __init__(self) -> None:
        self.name = ""
        self.shape = None # used to show the tandem
        self.shape_filepath = ""
        self.tool_shape = None # used to boolean cut from the final product
        self.tool_filepath = ""
        self.offsets = [0.0, 0.0, 0.0] # translate offsets 
        self.rotation = [0.0] # rotation (0.0) along each axis xyz
    
    def fromDict(self, data:dict) -> None:
        self.name = data["Tandem Name"]
        
        # shapes
        self.shape_filepath = data["Display Model File"]
        self.tool_filepath = data["Tool Model File"]
        
        # model shapes need to be loaded from elsewhere

    def toDict(self) -> str:
        return {self.name: {
            "Tandem Name": self.name,
            "Display Model File": self.shape_filepath,
            "Tool Model File": self.tool_filepath}}