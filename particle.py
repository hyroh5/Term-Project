from pygame.math import Vector2

class Particle:
    def __init__(self, pos, vel, radius=7):
        self.pos = Vector2(pos)
        self.vel = Vector2(vel)
        self.acc = Vector2(0, 0)
        self.radius = radius

    def apply_force(self, f):
        self.acc += f

    # 중력 + 마찰력
    def compute_acc(self, gravity, drag):
        return gravity + (-drag * self.vel)

    # VerLet Integration
    def integrate(self, dt, gravity, drag):
        self.pos += self.vel * dt + 0.5 * self.acc * dt * dt
        new_acc = self.compute_acc(gravity, drag)
        self.vel += 0.5 * (self.acc + new_acc) * dt
        self.acc = new_acc
