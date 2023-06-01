from pygame import Rect
import pygame
import sys

def main():
    pygame.init()
    
    surface = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    
    running = True
    
    tile_amount = 25
    tile_gap = 2
    
    ore_patch = OrePatch(3, 3)
    miner = Miner(3, 3)
    belt = Belt(2, 3, Vec2(0, 1))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                bigger_size = max(event.w, event.h)
                bigger_size = 800 if bigger_size > 800 else bigger_size
                surface = pygame.display.set_mode((bigger_size, bigger_size), pygame.RESIZABLE)

        surface_width = surface.get_width()
        surface_height = surface.get_height()
        tile_width = 1 if surface_width < tile_amount else round(surface_width / tile_amount)
        tile_height = 1 if surface_height < tile_amount else round(surface_height / tile_amount)
        
        ore = miner.mine([ore_patch])
        if ore is not None:
            ore.x = 2
            belt.move_ore(ore)
            
        
        surface.fill(0x000000)
        for x in range(0, surface_width, tile_width):
            for y in range(0, surface_height, tile_height):
                surface.fill(0x86c06c, Rect(x + tile_gap, y + tile_gap, tile_width - tile_gap, tile_height - tile_gap))
                surface.fill(0x2f6951, Rect((ore_patch.x * tile_width) + tile_gap, (ore_patch.y * tile_height) + tile_gap, tile_width - tile_gap, tile_height - tile_gap))
                surface.fill(0xffffff, Rect((miner.x * tile_width) + 4, (miner.y * tile_height) + 4, tile_width - 8, tile_height - 8))
                surface.fill(0xff00ff, Rect((belt.x * tile_width) + 4, (belt.y * tile_height) + 4, tile_width - 8, tile_height - 8))
                if ore is not None:
                    surface.fill(0x000000, Rect((ore.x * tile_width) + 4, (ore.y * tile_height) + 4, tile_width - 8, tile_height - 8))
        
        pygame.display.update()

        clock.tick(60)

    pygame.quit()
    sys.exit()

class Vec2:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

class OrePatch:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        
class Ore:
    def __init__(self, x: int, y: int, amount: int) -> None:
        self.x = x
        self.y = y
        self.amount = amount
        
class Miner:
    def __init__(self, x: int , y: int) -> None:
        self.x = x
        self.y = y
    
    def mine(self, ore_patches: list[OrePatch]) -> Ore | None:
        if not list(filter(lambda ore: ore.x == self.x and ore.y == self.y, ore_patches)):
            return
        
        return Ore(self.x, self.y, 1)
        
class Belt:
    def __init__(self, x: int , y: int, speed: Vec2) -> None:
        self.x = x
        self.y = y
        #in coord/s
        self.speed = speed
        
    def move_ore(self, ore: Ore):
        if (ore.x != self.x or ore.y != self.y):
            return 
        
        ore.x += self.speed.x
        ore.y += self.speed.y

if __name__ == "__main__":
    main()