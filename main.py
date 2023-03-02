import sys
from pygame.math import Vector2
import random
import pygame

pygame.init()

cell_size = 20
cell_number = 20
screen = pygame.display.set_mode((cell_size*cell_number,cell_size*cell_number))
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf',25)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.foods = [FOOD(),FOOD(),FOOD()]
        for i in range(20):
            self.foods.append(FOOD())
        self.food = FOOD()
    
    def update(self):
        self.snake.snake_move()
        self.collision()
        self.check_fail()
    
    def draw_elements(self):
        self.draw_grass()
        for food in self.foods:
            food.draw_food()
        self.snake.draw_snake()
        self.draw_score()

    def collision(self):
        for food in self.foods:
            if food.pos == self.snake.body[0]:
                food.randomise()
                self.snake.add_block()
                self.snake.play_crunch_sound()
            
        for block in self.snake.body[1:]:
            if block == self.food.pos:
                self.food.randomise()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x <= cell_number:
            self.game_over()
        elif not 0 <= self.snake.body[0].y <= cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color = (167,209,61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x = int(cell_size*cell_number -60)
        score_y = int(cell_size*cell_number - 60)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple = pygame.image.load("assets/apple.png")
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width+score_rect.width,apple_rect.height+1)

        pygame.draw.rect(screen,(167,209,61),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen,(56,74,61),bg_rect,2)

class FOOD:
    def __init__(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x,self.y)
        self.apple = pygame.image.load("assets/apple.png").convert_alpha()
        self.apple = pygame.transform.scale(self.apple,(cell_size,cell_size))
    
    def draw_food(self):
        food_rect = pygame.Rect(int(self.x*cell_size),int(self.y*cell_size),cell_size,cell_size)
        # pygame.draw.rect(screen,(126,166,114),food_rect) NO NEED DIRECTLY IMAGE
        screen.blit(self.apple,food_rect)

    def randomise(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x,self.y)

class SNAKE:
    def __init__(self):
        self.body = [Vector2(7,10),Vector2(8,10),Vector2(9,10)]
        self.direction = Vector2(0,1)
        self.new_block = False

        self.head_up = pygame.image.load("assets/head_up.png").convert_alpha()
        self.head_up = pygame.transform.scale(self.head_up,(cell_size,cell_size))
        self.head_down = pygame.image.load("assets/head_down.png").convert_alpha()
        self.head_down = pygame.transform.scale(self.head_down,(cell_size,cell_size))
        self.head_right = pygame.image.load("assets/head_right.png").convert_alpha()
        self.head_right = pygame.transform.scale(self.head_right,(cell_size,cell_size))
        self.head_left = pygame.image.load("assets/head_left.png").convert_alpha()
        self.head_left = pygame.transform.scale(self.head_left,(cell_size,cell_size))

        self.tail_up = pygame.image.load("assets/tail_up.png").convert_alpha()
        self.tail_up = pygame.transform.scale(self.tail_up,(cell_size,cell_size))
        self.tail_down = pygame.image.load("assets/tail_down.png").convert_alpha()
        self.tail_down = pygame.transform.scale(self.tail_down,(cell_size,cell_size))
        self.tail_right = pygame.image.load("assets/tail_right.png").convert_alpha()
        self.tail_right = pygame.transform.scale(self.tail_right,(cell_size,cell_size))
        self.tail_left = pygame.image.load("assets/tail_left.png").convert_alpha()
        self.tail_left = pygame.transform.scale(self.tail_left,(cell_size,cell_size))

        self.body_vertical = pygame.image.load("assets/body_vertical.png").convert_alpha()
        self.body_vertical = pygame.transform.scale(self.body_vertical,(cell_size,cell_size))
        self.body_horizontal = pygame.image.load("assets/body_horizontal.png").convert_alpha()
        self.body_horizontal = pygame.transform.scale(self.body_horizontal,(cell_size,cell_size))

        self.body_tr = pygame.image.load("assets/body_tr.png").convert_alpha()
        self.body_tr = pygame.transform.scale(self.body_tr,(cell_size,cell_size))
        self.body_tl = pygame.image.load("assets/body_tl.png").convert_alpha()
        self.body_tl = pygame.transform.scale(self.body_tl,(cell_size,cell_size))
        self.body_br = pygame.image.load("assets/body_br.png").convert_alpha()
        self.body_br = pygame.transform.scale(self.body_br,(cell_size,cell_size))
        self.body_bl = pygame.image.load("assets/body_bl.png").convert_alpha()
        self.body_bl = pygame.transform.scale(self.body_bl,(cell_size,cell_size))

        self.crunch_sound = pygame.mixer.Sound('Sound/Sound_crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index,block in enumerate(self.body):
            block_x = block.x * cell_size
            block_y = block.y * cell_size
            block_rect = pygame.Rect(block_x,block_y,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[len(self.body) - 2] - self.body[len(self.body) - 1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down
  
    def snake_move(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body = body_copy
            self.new_block = False 
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body = body_copy

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(7,10),Vector2(8,10),Vector2(9,10)]

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,110)
clock = pygame.time.Clock()

main = MAIN()
while True:
    screen.fill((167,200,61))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.USEREVENT:
            main.update()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main.snake.direction.y != 1:
                    main.snake.direction = Vector2(0,-1)
            elif event.key == pygame.K_RIGHT:
                if main.snake.direction.x != -1:
                    main.snake.direction = Vector2(1,0)
            elif event.key == pygame.K_LEFT:
                if main.snake.direction.x != 1:
                    main.snake.direction = Vector2(-1,0)
            elif event.key == pygame.K_DOWN:
                if main.snake.direction.y != -1:
                    main.snake.direction = Vector2(0,1)
    
    main.draw_elements()
    clock.tick(60)
    pygame.display.update()