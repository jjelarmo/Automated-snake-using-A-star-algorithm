import pygame, sys, random
from pygame.math import Vector2
class FRUIT(object):
    def __init__(self):
        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(0, cell_number-1)
        self.pos = Vector2(self.x, self.y)
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size ,cell_size,cell_size)
        #screen.blit(apple,fruit_rect)
        pygame.draw.rect(screen, (255,0,0), fruit_rect)

class SNAKE(object):
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(5,11),Vector2(5,12)]
        self.direction = Vector2(1,0)
        self.stat = 'moving'
    def draw_snake(self):
        for block in self.body:
            snake_rect = pygame.Rect(block.x * cell_size, block.y * cell_size ,cell_size,cell_size)
            pygame.draw.rect(screen, (0,0,255), snake_rect)
    def move_snake_current(self):
        #self.direction = new_direction
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]
        self.stat = 'moving'
    def move_snake_new(self, new_direction):
        if self.direction.x + new_direction.x !=0 or self.direction.y + new_direction.y !=0 :
            self.direction = new_direction
            self.move_snake_current()
            self.stat = 'moving'
            
class GAME(object):
    def __init__(self):
        self.fruit = FRUIT()
        self.snake = SNAKE()
        self.status = 'stop'
    def update_current(self):
        self.snake.move_snake_current()
        self.check_fruit()
    def update_new(self, new_direction):
        self.snake.move_snake_new(new_direction)
        self.check_fruit()
    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
    def check_fruit(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.body.append(self.fruit.pos)
            del self.fruit
            self.fruit = FRUIT()
            self.snake.stat = 'eating'
    def collision(self,cell_number):
        head = self.snake.body[0]
        if self.snake.stat == 'moving':
            if head.x<=-1 or head.x>=cell_number+1 or head.y<=-1 or head.y>=cell_number+1:
                self.game_over()
            for block in self.snake.body[1:]:
                if self.snake.body[0] == block:
                    self.game_over()
    def game_over(self):
        pygame.quit()
        sys.exit()
        
            
pygame.init()
cell_size = 20
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size)) #origin top left corner
clock = pygame.time.Clock()
apple = pygame.image.load('apple.png').convert_alpha()
main_game = GAME()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE and main_game.status == 'play':
            main_game.update_current()
            main_game.collision(cell_number)
        if event.type == pygame.KEYDOWN:
            if main_game.status == 'stop' and event.key== pygame.K_SPACE:
                main_game.status = 'play'
            if main_game.status == 'play' and event.key == pygame.K_UP:
                main_game.update_new(Vector2(0,-1))
            if main_game.status == 'play' and event.key == pygame.K_DOWN:
                main_game.update_new(Vector2(0,1))
            if main_game.status == 'play' and event.key == pygame.K_LEFT:
                main_game.update_new(Vector2(-1,0))
            if main_game.status == 'play' and event.key == pygame.K_RIGHT:
                main_game.update_new(Vector2(1,0))
    screen.fill((175,215,70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
