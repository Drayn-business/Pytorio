from dataclasses import dataclass
from pygame import Rect
import pygame
import sys
import math
import copy

@dataclass
class Vec2:
    x: int
    y: int

@dataclass
class OrePatch: 
    x: int 
    y: int
        
@dataclass
class Ore:
    x: int 
    y: int
    locked: bool = False
        
@dataclass
class Belt:
    x: int
    y: int
    speed: Vec2

@dataclass
class Miner:
    x: int
    y: int

@dataclass
class Hub:
    x: int
    y: int
    width: int
    height: int

def move_ore(node: Belt, ore: Ore) -> None:
        if ore.x != node.x or ore.y != node.y or ore.locked == True:
            return 
           
        ore.x += node.speed.x
        ore.y += node.speed.y
        ore.locked = True

def mine(node: Miner, ore_patches: list[OrePatch], belt_buffer: list[Belt]) -> Ore | None:
        if not list(filter(lambda ore: ore.x == node.x and ore.y == node.y, ore_patches)):
            return
        
        near_belt = list(filter(lambda belt: belt.x == node.x + 1 or belt.x == node.x - 1 or belt.y == node.y + 1 or belt.y == node.y - 1, belt_buffer))
        
        return Ore(node.x, node.y) if not near_belt else Ore(near_belt[0].x, near_belt[0].y, True)

def pickup(node: Hub, ore: Ore, ore_buffer: list[Ore]) -> int:
    if (not ore.x in range(node.x, node.x + node.width) or not ore.y in range(node.y, node.y + node.height)):
        return 0
    
    ore_buffer.remove(ore)
    return 1

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
    hub = Hub(3, 5, 3, 3)
    
    rotation = Vec2(0, 1)

    #game loop
    while running:
        surface_size = surface.get_width()
        tile_size = 1 if surface_size < tile_amount else round(surface_size / tile_amount)
        
        #event listener
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.key.key_code("r"):
                    if rotation.x != 0:
                        rotation.y = rotation.x
                        rotation.x = 0
                    elif rotation.y != 0:
                        rotation.x = rotation.y * -1
                        rotation.y = 0
                        
            if event.type == pygame.VIDEORESIZE:
                bigger_size = max(event.w, event.h)
                if bigger_size > 800: bigger_size = 800
                elif bigger_size < 400: bigger_size = 400
                surface = pygame.display.set_mode((bigger_size, bigger_size), pygame.RESIZABLE)
                surface_size = surface.get_width()
                tile_size = 1 if surface_size < tile_amount else round(surface_size / tile_amount)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                rel_x = math.floor(pos[0]/tile_size)
                rel_y = math.floor(pos[1]/tile_size)
                existing_belt = list(filter(lambda belt: rel_x == belt.x and rel_y == belt.y, belt_buffer))
                
                if existing_belt and existing_belt[0].speed != rotation:
                    belt_buffer.remove(existing_belt[0])
                    belt_buffer.append(Belt(rel_x, rel_y, copy.copy(rotation))) 
                elif not existing_belt:
                    belt_buffer.append(Belt(rel_x, rel_y, copy.copy(rotation))) 
                        
        #belt movement
        if frame_counter == 60:
            ore = mine(miner, [ore_patch], belt_buffer)
            if ore is not None and ore not in ore_buffer:
                ore_buffer.append(ore)
        
            for o in ore_buffer:
                for b in belt_buffer:
                    if o.locked: continue
                    move_ore(b, o)
                    
                obtained_ore += pickup(hub, o, ore_buffer)
        
            print(obtained_ore)
        
        #render
        
        surface.fill(0x000000)
        for x in range(0, surface_size, tile_size):
            for y in range(0, surface_size, tile_size):
                surface.fill(0x86c06c, Rect(x + tile_gap, y + tile_gap, tile_size - tile_gap, tile_size - tile_gap))
                surface.fill(0x2f6951, Rect((ore_patch.x * tile_size) + tile_gap, (ore_patch.y * tile_size) + tile_gap, tile_size - tile_gap, tile_size - tile_gap))
                
                for b in belt_buffer:
                    surface.fill(0xff00ff, Rect((b.x * tile_size) + 4, (b.y * tile_size) + 4, tile_size - 8, tile_size - 8))
                for o in ore_buffer:
                    surface.fill(0x000000, Rect((o.x * tile_size) + 6, (o.y * tile_size) + 6, tile_size - 12, tile_size - 12))
                
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

if __name__ == "__main__":
    main()