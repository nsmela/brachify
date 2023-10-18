class TandemModel:
    def __init__(self) -> None:
        self.name = ""
        self.shape_filepath = ""

    def fromDict(self, data: dict) -> None:
        self.name = data["Tandem Name"]

        # shapes
        self.shape_filepath = data["Model File"]

    def toDict(self) -> str:
        return {self.name: {
            "Tandem Name": self.name,
            "Model File": self.shape_filepath}}

