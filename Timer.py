class Timer:
    
    def __init__(self):
        self.time = 0
        self.start_time = None
        self.is_pause = False
        self.ticks_func = None

    def set_ticks_func(self, func):
        self.ticks_func = func

    def reset(self):
        self.start_time = self.ticks_func()
        self.time = 0

    def update(self):
        if not self.is_pause:
            self.time = self.ticks_func() - self.start_time

    def pause(self):
        self.is_pause = True
        self.pause_time = self.ticks_func()

    def unpause(self):
        self.is_pause = False
        self.start_time += self.ticks_func() - self.pause_time

    def get_time(self):
        return self.time/1000.

