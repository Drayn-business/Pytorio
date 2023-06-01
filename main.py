from pygame import Rect
import pygame
import sys

def main():
    pygame.init()
    
    surface = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    
    running = True
    max_fps = 60
    frame_counter = 0
    
    tile_amount = 25
    tile_gap = 2
    
    obtained_ore = 0
    
    ore_patch = OrePatch(3, 3)
    miner = Miner(3, 3)
    belt_buffer: list[Belt] = [Belt(2, 3, Vec2(0, 1)), Belt(2, 4, Vec2(0, 1)), Belt(2, 5, Vec2(1, 0))]
    ore_buffer: list[Ore] = []
    hub = Collector(3, 5, 3, 3)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                bigger_size = max(event.w, event.h)
                if bigger_size > 800: bigger_size = 800
                elif bigger_size < 400: bigger_size = 400
                surface = pygame.display.set_mode((bigger_size, bigger_size), pygame.RESIZABLE)

        surface_size = surface.get_width()
        tile_size = 1 if surface_size < tile_amount else round(surface_size / tile_amount)
        
        
        if frame_counter == 60:
            ore = miner.mine([ore_patch])
            if ore is not None:
                ore_buffer.append(ore)
        
            for o in ore_buffer:
                
                if o.x == 3 and o.y == 3:
                    o.x = 2
                    o.locked = True
                    
                for b in belt_buffer:
                    if o.locked: continue
                    b.move_ore(o)
                    
                obtained_ore += hub.pickup(o, ore_buffer)
        
            print(obtained_ore)
        
        surface.fill(0x000000)
        for x in range(0, surface_size, tile_size):
            for y in range(0, surface_size, tile_size):
                surface.fill(0x86c06c, Rect(x + tile_gap, y + tile_gap, tile_size - tile_gap, tile_size - tile_gap))
                surface.fill(0x2f6951, Rect((ore_patch.x * tile_size) + tile_gap, (ore_patch.y * tile_size) + tile_gap, tile_size - tile_gap, tile_size - tile_gap))
                
                for b in belt_buffer:
                    surface.fill(0xff00ff, Rect((b.x * tile_size) + 4, (b.y * tile_size) + 4, tile_size - 8, tile_size - 8))
                for o in ore_buffer:
                    surface.fill(0x000000, Rect((o.x * tile_size) + 4, (o.y * tile_size) + 4, tile_size - 8, tile_size - 8))
                
                surface.fill(0xffffff, Rect((miner.x * tile_size) + 4, (miner.y * tile_size) + 4, tile_size - 8, tile_size - 8))
                surface.fill(0x00ffff, Rect((hub.x * tile_size) + 4, (hub.y * tile_size) + 4, (tile_size * hub.width) - 8, (tile_size * hub.height) - 8))
        
        pygame.display.update()

        for o in ore_buffer:
            o.locked = False

        frame_counter += 1
        if frame_counter > max_fps:
            frame_counter = 0
        clock.tick(max_fps)

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
    def __init__(self, x: float, y: float, amount: int, locked: bool = False) -> None:
        self.x = x
        self.y = y
        self.amount = amount
        self.locked = locked
        
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
        
    def move_ore(self, ore: Ore) -> None:
        if ore.x != self.x or ore.y != self.y or ore.locked == True:
            return 
           
        ore.x += self.speed.x
        ore.y += self.speed.y
        ore.locked = True
        
class Collector:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def pickup(self, ore: Ore, ore_buffer: list[Ore]) -> int:
        if (not ore.x in range(self.x, self.x + self.width) or not ore.y in range(self.y, self.y + self.height)):
            return 0
        
        ore_buffer.remove(ore)
        return 1

if __name__ == "__main__":
    main()