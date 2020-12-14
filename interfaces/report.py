import pandas as pd


class Report():

    def __init__(self):
        self.df = None
        
    def initialize(self):
        raise NotImplementedError
    
    def generate(self, strategies: list, df: pd.DataFrame):
        raise NotImplementedError