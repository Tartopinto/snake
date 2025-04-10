# main.py

import pygame
import sys
import random
import config
from game.snake import Snake
from game.food import Food

from score_manager import get_top_scores

def game_over_screen(screen):
    screen.fill((30, 30, 30))
    center = (config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 - 80)
    radius = 80

    # Circle with arrow
    pygame.draw.circle(screen, (255, 255, 255), center, radius, 5)
    pygame.draw.arc(screen, (255, 255, 255), (center[0]-50, center[1]-50, 100, 100), 3.8, 6.0, 5)
    pygame.draw.polygon(screen, (255, 255, 255), [
        (center[0]+35, center[1]+20),
        (center[0]+50, center[1]+5),
        (center[0]+30, center[1])
    ])

    # Text instructions
    font = pygame.font.Font(None, 36)
    text = font.render("Press R to retry or Q to quit", True, (200, 200, 200))
    screen.blit(text, (center[0] - text.get_width() // 2, center[1] + radius + 20))

    # Top scores — centered below the circle
    small_font = pygame.font.Font(None, 32)
    top_scores = get_top_scores()

    score_start_y = center[1] + radius + 100  # 60 px below the circle
    
    for i, score in enumerate(top_scores):
        score_text = small_font.render(f"{i+1}. {score} food", True, config.FOOD_COLOR)
        screen.blit(score_text, (center[0] - score_text.get_width() // 2, score_start_y + i * 30))


    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return "quit"
                elif event.key == pygame.K_r:
                    return "restart"



def main():


    while True:  # Allow restarting
        arena_margin = 0
        arena_shrink_step = config.BLOCK_SIZE  # how much the arena shrinks each time
        arena_rect = pygame.Rect(
            arena_margin,
            arena_margin,
            config.WINDOW_WIDTH - 2 * arena_margin,
            config.WINDOW_HEIGHT - 2 * arena_margin
        )   
        food_counter = 0  # Initialize the food eaten counter   
        pygame.init()

        screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption(config.WINDOW_TITLE)

        clock = pygame.time.Clock()
        snake = Snake()
        food = Food(snake, arena_rect)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                        snake.change_direction(event.key)

            snake.move()
            from score_manager import save_score

            # Check for collision with the border or the snake itself
            if snake.check_collision(arena_rect):
                save_score(food_counter)  # Save current score
                result = game_over_screen(screen)
                if result == "quit":
                    pygame.quit()
                    exit()
                elif result == "restart":
                    running = False  # Breaks inner loop, restarts outer loop
                break

            # Check if the snake's head collides with the food
            head_x, head_y = snake.head_position()
            if (head_x < food.x + food.size and head_x + config.BLOCK_SIZE > food.x and
                head_y < food.y + food.size and head_y + config.BLOCK_SIZE > food.y):
                
                if food_counter % 3 == 0 and food_counter > 0 and food_counter < 20:
                    arena_margin += arena_shrink_step
                    arena_rect = pygame.Rect(
                        arena_margin,
                        arena_margin,
                        config.WINDOW_WIDTH - 2 * arena_margin,
                        config.WINDOW_HEIGHT - 2 * arena_margin
                    )
                    if snake.check_collision_after_shrink(arena_rect):
                        save_score(food_counter)  # Save current score
                        result = game_over_screen(screen)
                        if result == "quit":
                            pygame.quit()
                            exit()
                        elif result == "restart":
                            running = False  # Breaks inner loop, restarts outer loop
                        break
                food.spawn_new_food(snake, arena_rect)  # Reposition food
                snake.grow()  # Grow the snake
                food_counter += 1  # Increase the food eaten counter
                
                

            # Draw everything
            screen.fill(config.DARK_GREY)

            # Draw the border
            pygame.draw.rect(
                screen,
                config.BORDER_COLOR,
                arena_rect,
                config.BORDER_THICKNESS
            )

            # Draw the snake and food
            snake.draw(screen)
            food.draw(screen)

            # Draw the counter
            font = pygame.font.SysFont('Arial', 30)  # Create a font object
            food_text = font.render(f'Food: {food_counter}', True, config.FOOD_COLOR)  # Create the text surface

            # Create a semi-transparent background for the counter
            counter_width = food_text.get_width() + 20  # Add some padding
            counter_height = food_text.get_height() + 10  # Add some padding
            counter_surface = pygame.Surface((counter_width, counter_height), pygame.SRCALPHA)  # Create a transparent surface
            counter_surface.fill((0, 0, 0, 128))  # Semi-transparent black background (RGBA)

            # Blit the text onto the counter surface
            counter_surface.blit(food_text, (10, 5))  # Position the text on the surface

            # Draw the counter background and text on the screen
            screen.blit(counter_surface, (config.WINDOW_WIDTH - counter_width - 10, 10))  # Position it in the top-right corner

            pygame.display.flip()
            clock.tick(10)


if __name__ == "__main__":
    main()
