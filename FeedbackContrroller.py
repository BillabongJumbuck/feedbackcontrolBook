DT = 0.01

class PidController:
    def __init__(self, kp, ki, kd=0):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.i = 0
        self.d = 0
        self.prev = 0

    def work(self, e):
        self.i += e*DT
        self.d = (e - self.prev) / DT
        self.prev = e

        return self.kp*e + self.ki*self.i + self.kd*self.d