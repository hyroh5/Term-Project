import pygame
from pygame.math import Vector2
from waterscene import WaterScene

pygame.init()

W, H = 900, 600
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

scene = WaterScene(W, H)

radius = 6
bubble = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
pygame.draw.circle(bubble, (95, 150, 255, 170), (radius, radius), radius)

running = True
while running:
    dt = clock.tick(60) / 1000

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            scene.emitter = Vector2(e.pos)

    scene.update(dt)

    screen.fill((12, 15, 28))

    pygame.draw.line(screen, (240, 240, 240), scene.ramp_a, scene.ramp_b, 6)

    for p in scene.particles:
        screen.blit(bubble, (p.pos.x - radius, p.pos.y - radius))

    pygame.display.flip()

pygame.quit()
