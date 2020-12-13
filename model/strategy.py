from config import OPEN_POSITION, CLOSE_POSITION, NO_EVENT

class Strategy():

    def __init__(self, name, open_position_param, close_position_param, position):
        self.name = name
        self.open_position = open_position_param
        self.close_position = close_position_param
        self.position = position
        self.have_position = False
        self.entry_index = None
        
    def check_event(self, data, current_index):       
        if not self.have_position:  # check for open position
            rule_triggered = self.check_rules(data, current_index, self.open_position.rules)
            if rule_triggered:
                self.have_position = True
                self.entry_index = current_index
                return OPEN_POSITION, rule_triggered
            
        else:  # check for close positioin
            rule_triggered = self.check_rules(data, current_index, self.close_position.rules)
            if rule_triggered:
                self.have_position = False
                self.entry_index = None
                return CLOSE_POSITION, rule_triggered
        
        return NO_EVENT, None
    
    def check_rules(self, data, current_index, rules):
        # logical OR on all the rules
        for rule in rules:
            try:
                if rule.f(data, rule.ref, self.entry_index, current_index):
                    return rule.name
            except Exception as e:
                print('[ERROR] {} {} {}'.format(current_index, rule.name, e))
        return False