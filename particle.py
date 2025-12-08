from pygame.math import Vector2

class Particle:
    def __init__(self, pos, vel, radius=7):
        self.pos = Vector2(pos)
        self.vel = Vector2(vel)
        self.acc = Vector2(0, 0)
        self.radius = radius

    def apply_force(self, f):
        self.acc += f

    def integrate(self, dt):
        self.vel += self.acc * dt
        self.pos += self.vel * dt
        self.acc.xy = (0, 0)
