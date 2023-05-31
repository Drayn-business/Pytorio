from pygame import Rect
import pygame
import random
import sys
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    running = True
    counter = 30
    
    tile_amount = 25
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    tile_width = math.ceil(screen_width / tile_amount) if screen_width < tile_amount else round(screen_width / tile_amount)
    tile_height = math.ceil(screen_height / tile_amount) if screen_height < tile_amount else round(screen_height / tile_amount)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                counter = 30

        if counter == 30:
            counter = 0
            for x in range(0, screen_width, tile_width):
                for y in range(0, screen_height, tile_height):
                    screen.fill(random.randint(0, 0xFFFFFF), Rect(x, y, tile_width, tile_height))
        
        pygame.display.update()

        counter += 1
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()