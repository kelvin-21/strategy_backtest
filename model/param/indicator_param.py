class IndicatorParam():
    def __init__(self, name):
        self.name = name
        
    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.__dict__ == other.__dict__