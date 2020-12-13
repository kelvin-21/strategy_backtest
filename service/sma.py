class SMA():
    
    def __init__(self, param):
        self.param = self.param
        
    def compute(self, data):
        
        data[self.param.name] = data[self.param.on].rolling(window=self.param.period).mean()
        
        return data