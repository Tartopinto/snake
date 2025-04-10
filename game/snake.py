# game/snake.py

import pygame
import config

from collections import deque

class Snake:
    def __init__(self):
        self.block_size = config.BLOCK_SIZE
        self.color = config.LIGHT_YELLOW
        self.length = config.INITIAL_SNAKE_LENGTH

        start_x = config.WINDOW_WIDTH // 2
        start_y = config.WINDOW_HEIGHT // 2

        self.body = []
        for i in range(self.length):
            self.body.append((start_x - i * self.block_size, start_y))

        self.direction = (self.block_size, 0)  # initially moving right
        self.direction_queue = deque()  # queued directions

    def move(self):
        # Apply next valid direction from queue
        while self.direction_queue:
            next_dir = self.direction_queue.popleft()
            if (next_dir[0] != -self.direction[0] or next_dir[1] != -self.direction[1]):
                self.direction = next_dir
                break

        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        self.body.pop()

    def change_direction(self, key):
        up = (0, -self.block_size)
        down = (0, self.block_size)
        left = (-self.block_size, 0)
        right = (self.block_size, 0)

        key_to_dir = {
            pygame.K_w: up,
            pygame.K_s: down,
            pygame.K_a: left,
            pygame.K_d: right
        }

        if key in key_to_dir:
            new_dir = key_to_dir[key]
            self.direction_queue.append(new_dir)

    def check_collision_after_shrink(self, arena_rect):
        head_x, head_y = self.body[0]

        # Check collision with the borders (after shrinking)
        bt = config.BORDER_THICKNESS
        collision = False

        if head_x < arena_rect.left + bt:
            # Push the snake to the left boundary
            head_x = arena_rect.left + 2*bt
            collision = True
        elif head_y < arena_rect.top + bt:
            # Push the snake to the top boundary
            head_y = arena_rect.top + 2*bt
            collision = True
        elif head_x + config.BLOCK_SIZE > arena_rect.right - bt:
            # Push the snake to the right boundary
            head_x = arena_rect.right - 2*bt - config.BLOCK_SIZE
            collision = True
        elif head_y + config.BLOCK_SIZE > arena_rect.bottom - bt:
            # Push the snake to the bottom boundary
            head_y = arena_rect.bottom - 2*bt - config.BLOCK_SIZE
            collision = True

        if collision:
            # Stop the snake's movement in the direction that caused the collision
            self.body[0] = (head_x, head_y)
            return False  # Don't trigger game over immediately

        # Check collision with the body (excluding the head itself)
        for segment in self.body[1:]:
            if segment == (head_x, head_y):
                return True

        return False
    def check_collision(self, arena_rect):
        head_x, head_y = self.body[0]

        # Check collision with the borders
        bt = config.BORDER_THICKNESS
        if (
            head_x < arena_rect.left + bt
            or head_y < arena_rect.top + bt
            or head_x + config.BLOCK_SIZE > arena_rect.right - bt
            or head_y + config.BLOCK_SIZE > arena_rect.bottom - bt
        ):
            return True

        # Check collision with the body (excluding the head itself)
        for segment in self.body[1:]:
            if segment == (head_x, head_y):
                return True

        return False


    def grow(self):
        """Add a new segment to the snake."""
        tail_x, tail_y = self.body[-1]
        self.body.append((tail_x, tail_y))  # Add new segment at the end

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(
                screen,
                self.color,
                pygame.Rect(segment[0], segment[1], self.block_size, self.block_size)
            )

    def head_position(self):
        return self.body[0]
