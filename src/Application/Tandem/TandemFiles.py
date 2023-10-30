class TandemFile:
    def __init__(self) -> None:
        self.name = ""
        self.shape_url = None
        self.tool_url = None
        self.offsets = [0, 0, 0]

    def toJson() -> dict:
        '''convert the class into a json format'''
        pass

    def fromJson(data) -> None:
        '''convert the class from json data'''
        pass

    def save() -> bool:
        '''save the tandem model to the disk'''
        # add or update, depends if already existing
        # json write or update
        pass

    def load(name: str) -> bool:
        '''load from the saved file based on the name'''
        # json read
        pass
