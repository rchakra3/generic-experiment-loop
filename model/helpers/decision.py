import random


class Decision(object):

    def __init__(self, name, min_val, max_val):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val

    def generate_valid_val(self):
        return random.uniform(self.min_val, self.max_val)

    def get_range(self):
        return (self.min_val, self.max_val)
