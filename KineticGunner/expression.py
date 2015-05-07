
class Expression:
    def __init__(self, amount, dur ):
        self.total = amount
        self.change = self.total
        self.duration = dur
        self.time = 0.0

    def tick(self, dt):
        remaining = (self.duration - self.time)
        if remaining < 0.01:
            rate = self.total / self.duration
        else:
            rate = self.change / remaining
        self.change -= rate * dt
        self.time += dt
        return rate

    def complete(self):
        if self.time > self.duration:
            self.time = 0.0
            self.change = self.total
            return True
        else:
            return False