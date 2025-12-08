import random
from pygame.math import Vector2
from particle import Particle


class WaterScene:
    def __init__(self, w, h):
        self.w = w
        self.h = h

        self.particles = []
        self.max_particles = 1500

        self.gravity = Vector2(0, 900)
        self.drag = 0.12

        self.emitter = None
        self.flow_rate = 260 
        self.flow_acc = 0

        # 경사면 설정
        self.ramp_a = Vector2(0, h * 0.45)
        self.ramp_b = Vector2(w, h - 40)

        ab = self.ramp_b - self.ramp_a
        self.ramp_dir = ab.normalize()
        self.ramp_normal = Vector2(-self.ramp_dir.y, self.ramp_dir.x)

        self.ab = ab
        self.ab_len2 = ab.length_squared()

        dx = self.ramp_b.x - self.ramp_a.x
        dy = self.ramp_b.y - self.ramp_a.y
        self.m = dy / dx
        self.b_line = self.ramp_a.y - self.m * self.ramp_a.x

        self.x_min = min(self.ramp_a.x, self.ramp_b.x)
        self.x_max = max(self.ramp_a.x, self.ramp_b.x)


    # 물 생성 
    def spawn(self, dt):
        if not self.emitter:
            return
        if len(self.particles) >= self.max_particles:
            return

        # 초당 생성량
        self.flow_acc += self.flow_rate * dt
        n = int(self.flow_acc)
        self.flow_acc -= n

        for _ in range(n):
            if len(self.particles) >= self.max_particles:
                break

            offset = Vector2(
                random.uniform(-10, 10),
                random.uniform(-3, 3)    
            )

            vx = random.uniform(-8, 8)
            vy = random.uniform(-20, -5)  

            self.particles.append(
                Particle(self.emitter + offset, Vector2(vx, vy))
            )


    # 힘 적용
    def forces(self):
        for p in self.particles:
            p.apply_force(self.gravity)
            p.apply_force(-self.drag * p.vel)


    # 화면 경계 충돌
    def world_collision(self, p):
        r = p.radius

        if p.pos.y > self.h - r:
            p.pos.y = self.h - r
            if p.vel.y > 0:
                p.vel.y = 0

        if p.pos.x < r:
            p.pos.x = r
            if p.vel.x < 0:
                p.vel.x = 0

        if p.pos.x > self.w - r:
            p.pos.x = self.w - r
            if p.vel.x > 0:
                p.vel.x = 0


    # 경사면 충돌 + Tangent Sliding
    def ramp_collision(self, p):
        r = p.radius

        if p.pos.x < self.x_min or p.pos.x > self.x_max:
            return

        y_line = self.m * p.pos.x + self.b_line

        if p.pos.y + r > y_line:
            p.pos.y = y_line - r

            vn = p.vel.dot(self.ramp_normal)
            if vn < 0:
                p.vel -= vn * self.ramp_normal

            g_tan = self.gravity.dot(self.ramp_dir) * self.ramp_dir
            p.apply_force(g_tan)


    # 업데이트
    def update(self, dt):
        self.spawn(dt)
        self.forces()

        for p in self.particles:
            p.integrate(dt)
            self.world_collision(p)
            self.ramp_collision(p)
