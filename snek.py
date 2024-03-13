import pygame
import time
import random
import sys

# Game setup
# window
size_x = 720
size_y = 480
pygame.init()

# FPS (frames per second) controller
fps = pygame.time.Clock()
 
pygame.display.set_caption('Snek Score:0')
game_window = pygame.display.set_mode((size_x, size_y))

# Snake and fruit setup
# snake
snake_pos = [(size_x // 2, size_y // 2)]
snake_size = 1
# snake_speed = 10

class Snake:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.speed=10
        self.direction="RIGHT"
        self.score=0
        self.power_invincible=False
        self.active_power_time=0

    def draw(self):
        color=(0,255,0)
       
        for pos in self.pos:
            pygame.draw.rect(game_window, color, (pos[0], pos[1], 20, 20))
    
    def erase(self):
        color=(0,0,0)
        if self.power_invincible:
            color=(0,0,60)
        for pos in self.pos:
            pygame.draw.rect(game_window, color, (pos[0], pos[1], 20, 20))

    def grow(self):
        self.size+=1
        self.pos.append(self.pos[-1])

    def check_collision(self):
        for block in self.pos[1:]:
            if self.pos[0] == block:
                pygame.quit()
                sys.exit()
    
    def check_wall_collision(self):
        if self.pos[0][0] < 0 or self.pos[0][0] >= size_x or self.pos[0][1] < 0 or self.pos[0][1] >= size_y:
            pygame.quit()
            sys.exit()

    def check_fruit_collision(self):
        if pygame.Surface.get_at(game_window,(self.pos[0][0],self.pos[0][1]))==(255,0,0):
            self.grow()  
            self.score+=1
            pygame.display.set_caption(f"Snek Score:{self.score}")
            print(self.score)
        elif pygame.Surface.get_at(game_window,(self.pos[0][0],self.pos[0][1]))==(0,0,255):
            self.power_invincible=True
            self.active_power_time=time.time()
            game_window.fill((0,0,60))


    def update_pos(self):
        # prev=self.pos[0]
        new_pos=(0,0)
        if self.direction == "UP":
            new_pos = (self.pos[0][0], self.pos[0][1] - 20)
        elif self.direction == "DOWN":
            new_pos = (self.pos[0][0], self.pos[0][1] + 20)
        elif self.direction == "LEFT":
            new_pos = (self.pos[0][0] - 20, self.pos[0][1])
        elif self.direction == "RIGHT":
            new_pos = (self.pos[0][0] + 20, self.pos[0][1])
        
        if self.power_invincible==True:
            new_pos=(new_pos[0]%size_x,new_pos[1]%size_y)

        self.pos.insert(0,new_pos)
        self.pos.pop()

    def update(self):

        self.erase()
        # self.prev_pos=self.pos[0]
        

        self.update_pos()
            
        if self.power_invincible==False:
            # Check if snake collides with itself
            self.check_collision()
            # Check if snake collides with the wall
            self.check_wall_collision()
       #check if snake collides with fruit
        self.check_fruit_collision()

       
        # Draw the snake
        self.draw()


# fruit
def gen_random_coordinates():
    return (random.randint(0, size_x // 20) * 20, random.randint(0, size_y // 20) * 20)

fruit_pos = gen_random_coordinates()
fruit_spawn_time = time.time() # Time when the fruit was last spawned
pygame.draw.rect(game_window, (255, 0, 0), (fruit_pos[0], fruit_pos[1], 20, 20))

#Power_UP invincible for 5s power_up_1
invincible_fruit_pos=gen_random_coordinates()
invincible_fruit_spawn_time=fruit_spawn_time
pygame.draw.rect(game_window, (0, 0, 255), (invincible_fruit_pos[0], invincible_fruit_pos[1], 20, 20))
# Snake movement and frame updates
# direction = "RIGHT"
# change_to = direction


snake=Snake(snake_pos,snake_size)

# Game loop
while True:
    # game_window.fill((0, 0, 0))
    # Fruit spawn logic
    curr_time=time.time()
    if curr_time - fruit_spawn_time >= 5:  # Spawn a new fruit every 5 seconds
        fruit_pos = gen_random_coordinates()
        fruit_spawn_time = curr_time
        pygame.draw.rect(game_window, (255, 0, 0), (fruit_pos[0], fruit_pos[1], 20, 20))
    
    if curr_time - invincible_fruit_spawn_time >=20:
        invincible_fruit_pos=gen_random_coordinates()
        invincible_fruit_spawn_time=curr_time 
        pygame.draw.rect(game_window, (0, 0, 255), (invincible_fruit_pos[0], invincible_fruit_pos[1], 20, 20))

    if snake.power_invincible==True and curr_time-snake.active_power_time >5:
        snake.power_invincible=False
        game_window.fill((0,0,0))

    # Draw the fruit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != "DOWN":
                snake.direction = "UP"
            elif event.key == pygame.K_DOWN and snake.direction != "UP":
                snake.direction = "DOWN"
            elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                snake.direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                snake.direction = "RIGHT"

    # Update snake direction
    # direction = change_to

    # Update snake position and check for collisions
    snake.update()

    pygame.display.update()

    fps.tick(snake.speed)