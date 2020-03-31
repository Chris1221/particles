import pygame
import numpy as np
from settings import Settings
from agent import Agent, resolve_collisions

pygame.init()
conf = Settings()
screen = pygame.display.set_mode((conf.width, conf.height))
clock = pygame.time.Clock()
FPS = 60

n = 50
agents = [Agent(conf) for i in range(n)]
agents.append(Agent(conf, infected=True))

while True:
    clock.tick(FPS)

    nfine = 0
    ninfected = 0
    nimmune = 0
    ndead = 0

    for a in agents:
        if not a.dead and not a.infected and not a.immune:
            nfine += 1
        if not a.dead and a.infected:
            ninfected += 1
        if not a.dead and a.immune:
            nimmune += 1
        if a.dead:
            ndead += 1

    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    text_fine = font.render(str(nfine), True, (255,255,255))
    text_infected = font.render(str(ninfected), True, (255,0,0))
    text_immune = font.render(str(nimmune), True, (0,204,102))
    text_dead = font.render(str(ndead), True, (102,0,0))



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill((0, 0, 0))

    screen.blit(text_fine, (0,0))
    screen.blit(text_infected, (50, 0))
    screen.blit(text_immune, (100, 0))
    screen.blit(text_dead, (150, 0))

    resolve_collisions(agents, dist=conf.distance, prob=conf.probability)
    for a in agents:
        a.update()
        a.draw(screen)
    pygame.display.update()
