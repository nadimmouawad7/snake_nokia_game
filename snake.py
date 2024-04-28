import pygame
import sys
import random

pygame.init()

# Constants for the game
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (107, 142, 35)
SNAKE_COLOR = (0, 0, 0)
FOOD_COLOR = (0, 0, 0)

# Initialize screen and font
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)  # Default font and size

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (0, -1)
        self.growing = False

    def head_position(self):
        return self.positions[0]
        
    def change_direction(self, new_direction):
        opposite_direction = (-self.direction[0], -self.direction[1])
        if new_direction != opposite_direction:
            self.direction = new_direction

    def move(self, food):
        new_head = (self.head_position()[0] + self.direction[0], self.head_position()[1] + self.direction[1])

        # Wrap-around behavior
        new_head = ((new_head[0] % GRID_WIDTH), (new_head[1] % GRID_HEIGHT))

        # Check for collision with tail
        if new_head in self.positions:
            return "hit_tail"

        self.positions.insert(0, new_head)
        if self.head_position() == food:
            return "ate_food"
        if not self.growing:
            self.positions.pop()
        self.growing = False
        return "moved"

    def draw(self):
        for segment in self.positions:
            draw_object(segment, SNAKE_COLOR)

        # Draw eyes on the head
        head = self.positions[0]
        eye_size = GRID_SIZE // 10
        eye1_pos = (head[0] * GRID_SIZE + GRID_SIZE // 4, head[1] * GRID_SIZE + GRID_SIZE // 4)
        eye2_pos = (head[0] * GRID_SIZE + 3 * GRID_SIZE // 4, head[1] * GRID_SIZE + GRID_SIZE // 4)
        pygame.draw.circle(screen, WHITE, eye1_pos, eye_size)
        pygame.draw.circle(screen, WHITE, eye2_pos, eye_size)

def draw_object(position, color):
    block = pygame.Rect(position[0] * GRID_SIZE, position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, color, block)

def random_position():
    return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

def game_over_screen():
    game_over_text = font.render("Game Over", True, WHITE)
    retry_text = font.render("Retry (R)", True, WHITE)
    exit_text = font.render("Exit (E)", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 3))
    screen.blit(retry_text, (WIDTH // 2 - 100, HEIGHT // 2))
    screen.blit(exit_text, (WIDTH // 2 - 100, HEIGHT // 2 + 40))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                elif event.key == pygame.K_e:
                    pygame.quit()
                    sys.exit()

def main():
    snake = Snake()
    food = random_position()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.change_direction((1, 0))


        move_result = snake.move(food)
        if move_result == "hit_tail":
            game_over_screen()
            break
        elif move_result == "ate_food":
            food = random_position()
            snake.growing = True

        screen.fill(BACKGROUND_COLOR)
        draw_object(food, FOOD_COLOR)
        snake.draw()
        pygame.display.update()
        clock.tick(10)

if __name__ == "__main__":
    main()
