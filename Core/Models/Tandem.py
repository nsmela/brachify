class TandemModel:
    def __init__(self) -> None:
        self.name = ""
        self.shape = None  # the shape used to cut from the model
        self.shape_filepath = ""
        self.offsets = [0.0, 0.0, 0.0]  # translate offsets
        self.rotation = [0.0]  # rotation (0.0) along each axis xyz

    def fromDict(self, data: dict) -> None:
        self.name = data["Tandem Name"]

        # shapes
        self.shape_filepath = data["Model File"]

        # model shapes need to be loaded from elsewhere

    def toDict(self) -> str:
        return {self.name: {
            "Tandem Name": self.name,
            "Model File": self.shape_filepath}}
