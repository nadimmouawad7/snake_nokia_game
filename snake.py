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
BACKGROUND_COLOR = (0, 255, 0)  
SNAKE_COLOR = (0, 0, 0)      
FOOD_COLOR = (0, 0, 0)          
APPLE_COLOR = (255, 0, 0)       



# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        self.direction = (0, -1)
        self.growing = False

    def head_position(self):
        return self.positions[0]

    def move(self, food, red_apple):
        new_head = (self.head_position()[0] + self.direction[0], self.head_position()[1] + self.direction[1])

        if (new_head in self.positions or new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or new_head == red_apple):
            raise Exception("Game over")
        else:
            self.positions.insert(0, new_head)
            if self.head_position() == food:
                return True
            if not self.growing:
                self.positions.pop()
            self.growing = False
        return False

    def draw(self):
        for segment in self.positions:  
            draw_object(segment, SNAKE_COLOR)
        
        # Draw eyes on the head
        head = self.positions[0]
        eye_size = GRID_SIZE // 10
        eye1_pos = (head[0]*GRID_SIZE + GRID_SIZE//4, head[1]*GRID_SIZE + GRID_SIZE//4)
        eye2_pos = (head[0]*GRID_SIZE + 3*GRID_SIZE//4, head[1]*GRID_SIZE + GRID_SIZE//4)
        pygame.draw.circle(screen, WHITE, eye1_pos, eye_size)
        pygame.draw.circle(screen, WHITE, eye2_pos, eye_size)


    def change_direction(self, new_direction):
        if (new_direction[0] * self.direction[0] == 0 and new_direction[1] * self.direction[1] == 0):
            self.direction = new_direction

def draw_object(position, color):
    block = pygame.Rect(position[0] * GRID_SIZE, position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, color, block)

def random_position():
    return (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))

loop_counter = 0

def main():

    global loop_counter

    snake = Snake()
    food = random_position()
    red_apple = random_position()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))

        try:
            if snake.move(food, red_apple):
                food = random_position()
                red_apple = random_position()
                snake.growing = True
        except:
            pygame.quit()
            sys.exit()
        
        loop_counter += 1
        if loop_counter >= 3 and random.randint(0, 5) == 0:  # Chance to spawn an apple
            apple_pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if apple_pos not in snake.positions:  
                draw_object(apple_pos, APPLE_COLOR)
                if snake.positions[0] == apple_pos:  # Snake eats the apple, game over
                    return
            loop_counter = 0

        screen.fill(BACKGROUND_COLOR)
        draw_object(food, FOOD_COLOR)
        draw_object(red_apple, APPLE_COLOR)
        snake.draw()
        pygame.display.update()
        clock.tick(10)

if __name__ == "__main__":
    main()
