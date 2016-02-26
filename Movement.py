class Movement:
    """Movement keeps track of the player's moves. Each move can only have up to
    a defined number of steps. """

    def __init__(self, steps=1):
        self.steps_taken = None
        self.steps = steps
        self.move = 'stationary'
        self.move_list = []

    def add_move(self, direction):
        self.move_list.append(direction)

    def get_next_move(self):
        if self.move_list == []:
            if self.steps_taken is not None:
                if self.steps_taken < self.steps:
                    self.steps_taken += 1
                else:
                    self.move = 'stationary'
        else:
            if (self.steps_taken == self.steps) or \
               (self.steps_taken is None):
                self.move = self.move_list.pop(0)
                self.steps_taken = 0
            else:
                self.steps_taken += 1

        return self.move
