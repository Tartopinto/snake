# game/food.py

import pygame
import random
import config

class Food:
    def __init__(self, snake, arena_rect):
        self.color = config.FOOD_COLOR
        self.size = config.BLOCK_SIZE  # Make the food the same size as the snake block
        self.spawn_new_food(snake, arena_rect)

    def spawn_new_food(self, snake, arena_rect):
        """Repositions the food randomly within the arena."""
        grid_width = (arena_rect.width - 2*self.size) // self.size  # Exclude the space for food size
        grid_height = (arena_rect.height - 2*self.size) // self.size  # Exclude the space for food size
        offset_x = arena_rect.left + self.size
        offset_y = arena_rect.top + self.size
        
        while True:
            # Make sure food is within the bounds and doesn't touch the border
            self.x = random.randint(0, grid_width - 1) * self.size + offset_x
            self.y = random.randint(0, grid_height - 1) * self.size + offset_y

            # Ensure food doesn't overlap with the snake's body
            if (self.x, self.y) not in snake.body:
                return (self.x, self.y)


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.size, self.size))
