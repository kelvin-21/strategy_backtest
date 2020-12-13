class OpenPositionParam():
    def __init__(self, rules):
        self.rules = rules  # rule: f(data, ref, self.entry_index, current_index) -> boolean