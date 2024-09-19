class Memory:

    def __init__(self, forget_threshold : int = 10, short_term=None, long_term=None):
        if long_term is None:
            self.long_term = []
        else: self.long_term = long_term
        if short_term is None:
            self.short_term = []
        else: self.short_term = short_term
        self.forget_threshold = forget_threshold
        self.visited_sites = []