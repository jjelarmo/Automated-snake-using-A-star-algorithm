import pygame, sys, random
from pygame.math import Vector2

class Node(object):
    def __init__(self,inx,iny):
        self.coordinates= Vector2(inx, iny)
        self.status = "available"
        self.predecessor = None
        self.fn = 999
        self.gn = 999   #step
        self.hn = 999   #heurestics

    def calculate_hn(self,other):
        self.hn = int(((self.x - other.x)**2 + (self.y - other.y)**2 )**0.5)

    def calculate_fn(self):
        self.fn = self.gn + self.hn

    def __eq__(self, other):
        return self.coordinates.x == other.coordinates.x and self.coordinates.y == other.coordinates.y
    
    def __lt__(self, other):
        return self.fn < other.fn

    def __add__(self, other):
        return Node(self.coordinates.x + other.coordinates.x , self.coordinates.y + other.coordinates.y)
    
class BOX(object):
    def __init__(self,x,y):
        self.field = Node(x,y)
        self.field.status = "field"
        self.neighbors=[]

    def draw_box(self):
        field_box = pygame.Rect(self.field.coordinates.x * cell_size, self.field.coordinates.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (175,215,70), field_box)

    def find_neighbors(self,grid):
        x,y = int(self.field.coordinates.x), int(self.field.coordinates.y)
        potential_neighbors = [(x-1,y),(x,y-1), (x+1,y), (x,y+1)]
        for (new_x, new_y) in potential_neighbors:
            if new_x<=cell_number-1 and new_x>=0 and new_y<=cell_number-1 and new_y>=0:
                self.neighbors.append(grid[new_x][new_y])
        return self.neighbors
    
class FRUIT(object):
    def __init__(self):
        self.position = Node(random.randint(0, cell_number-1),random.randint(0, cell_number-1))
        self.position.status = "fruit"
        
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.position.coordinates.x * cell_size, self.position.coordinates.y * cell_size ,cell_size,cell_size)
        pygame.draw.rect(screen, (255,0,0), fruit_rect)

class SNAKE(object):
    def __init__(self):
        self.body = [Node(5,10),Node(5,11),Node(5,12)]
        for block in self.body:
            block.status = "snake"
        self.direction = Vector2(1,0)
        self.movement = "moving"
        
    def draw_snake(self):
        for block in self.body:
            snake_rect = pygame.Rect(block.coordinates.x * cell_size, block.coordinates.y * cell_size ,cell_size,cell_size)
            pygame.draw.rect(screen, (0,0,255), snake_rect)

    def convert_box_to_snake(self, new_part):
        pass
    
    def convert_fruit_to_snake(self, new_part):
        self.body.append(new_part)
        
    def move_snake_current(self):
        body_copy = self.body[:-1]
        
        new_field = BOX(self.body[-1].coordinates.x , self.body[-1].coordinates.y)
        new_field.draw_box()
        
        new_part_coordinates = self.body[0].coordinates + self.direction
        new_part=Node(new_part_coordinates.x,new_part_coordinates.y)
        new_part.status = "snake"
        body_copy.insert(0, new_part)
        self.body = body_copy[:]
        self.movement = "moving"
        
    def move_snake_new(self, new_direction):
        if self.direction.x + new_direction.x !=0 or self.direction.y + new_direction.y !=0 :
            self.direction = new_direction
            self.move_snake_current()
            self.movement = "moving"
            
class GAME(object):
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.update = 'stop'
        
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
        if self.fruit.position == self.snake.body[0]:
            self.fruit.position.status = "snake"
            self.snake.body.append(self.fruit.position)
            del self.fruit
            self.fruit = FRUIT()
            self.snake.movement = 'eating'
            
    def collision(self,cell_number):
        head = self.snake.body[0]
        if self.snake.movement == 'moving':
            if head.coordinates.x<=-1 or head.coordinates.x>=cell_number+1 or head.coordinates.y<=-1 or head.coordinates.y>=cell_number+1:
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
main_game = GAME()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

grid = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

for x in range(cell_number):
    for y in range(cell_number):
        grid[x][y] = BOX(x,y)
        grid[x][y].draw_box()
        
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE and main_game.update == 'play':
            main_game.update_current()
            main_game.collision(cell_number)
        if event.type == pygame.KEYDOWN:
            if main_game.update == 'stop' and event.key== pygame.K_SPACE:
                main_game.update = 'play'
            if main_game.update == 'play' and event.key == pygame.K_UP:
                main_game.update_new(Vector2(0,-1))
            if main_game.update == 'play' and event.key == pygame.K_DOWN:
                main_game.update_new(Vector2(0,1))
            if main_game.update == 'play' and event.key == pygame.K_LEFT:
                main_game.update_new(Vector2(-1,0))
            if main_game.update == 'play' and event.key == pygame.K_RIGHT:
                main_game.update_new(Vector2(1,0))
    
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
