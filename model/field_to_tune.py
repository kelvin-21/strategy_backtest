class FieldToTune():
    def __init__(self, name: str, low_bound, up_bound, step, extra_values=[]):
        self.name = name
        self.low_bound = low_bound
        self.up_bound  = up_bound
        self.step = step
        self.values = tuple(range(low_bound, up_bound, step)) + tuple(extra_values)