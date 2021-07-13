import pygame, sys, random
from pygame.math import Vector2
#import a_star

class Node(object):
    def __init__(self,inx,iny):
        self.coordinates= Vector2(inx, iny)
        self.neighbors=[]
        self.status = "available"
        self.predecessor = None
        self.fn = 999
        self.gn = 999   #step
        self.hn = 999   #heurestics

    def calculate_hn(self,other):
        self.hn = float(((self.coordinates.x - other.coordinates.x)**2 + (self.coordinates.y - other.coordinates.y)**2 )**0.5)

    def calculate_fn(self):
        self.fn = self.gn + self.hn

    def __eq__(self, other):
        return self.coordinates.x == other.coordinates.x and self.coordinates.y == other.coordinates.y
    
    def __lt__(self, other):
        return self.fn < other.fn

    def __add__(self, other):
        return Node(self.coordinates.x + other.coordinates.x , self.coordinates.y + other.coordinates.y)

    def __str__(self):
        return "x:" + str(self.coordinates.x) + " " + "y:" + str(self.coordinates.y) + "fn:" + str(self.fn)

    def find_neighbors(self,grid):
        x,y = int(self.coordinates.x), int(self.coordinates.y)
        potential_neighbors = [(x-1,y),(x,y-1), (x+1,y), (x,y+1)]
        for (new_x, new_y) in potential_neighbors:
            if new_x<=cell_number-1 and new_x>=0 and new_y<=cell_number-1 and new_y>=0:
                self.neighbors.append(grid[new_x][new_y])
        return self.neighbors

    def draw_box(self):
        field_box = pygame.Rect(self.coordinates.x * cell_size, self.coordinates.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (175,215,70), field_box)
        
class Stack(object):
    def __init__(self):
        self.data=[]
    
    def __len__(self):
        return len(self.data)

    def push(self, new_in):
        self.data.append(new_in)

    def pop(self):
        return self.data.pop(-1)

    def is_empty(self):
        return len(self.data)==0


class Heap(object):

    def __init__(self):
        self.data = []

    def root(self):
        return 0

    def __len__(self):
        return len(self.data)

    def is_empty(self):
        return len(self.data)==0
    
    def parent(self,j):
        return (j-1)//2

    def left(self,j):
        return 2*j+1

    def right(self,j):
        return 2*j+2

    def has_left(self,j):
        return self.left(j) < len(self)

    def has_right(self,j):
        return self.right(j) < len(self)

    def swap(self,i,j):
        self.data[i] , self.data[j] = self.data[j] , self.data[i]

    def upheap(self,j):
        i = self.parent(j)
        if j>0 and j<=(len(self)-1):
            if self.data[j] < self.data[i]:
                self.swap(j,i)
            self.upheap(i)

    def downheap(self,j):
        if self.has_left(j):
            child_index = self.left(j)

            if self.has_right(j):
                if self.data[self.right(j)] < self.data[child_index]:
                    child_index = self.right(j)

            if self.data[child_index] < self.data[j]:
                self.swap(child_index,j)
                self.downheap(child_index)
            
    def add(self,node):
        self.data.append(node)
        j=len(self.data)-1
        self.upheap(j)

    def remove_min(self):
        self.swap(0, len(self.data)-1)
        min_node = self.data.pop(-1)
        self.downheap(0)
        return min_node
    
class BOX(object):
    def __init__(self,x,y):
        self.field = Node(x,y)
        self.field.status = "field"
        self.neighbors=[]

    def draw_box(self):
        field_box = pygame.Rect(self.field.coordinates.x * cell_size, self.field.coordinates.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (175,215,70), field_box)
    
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
        
def search_path(grid, game):
    head=game.snake.body[0]
    destination = game.fruit.position

    print("head: " + str(head))
    print("destination: " + str(destination))
    closed_list = []
    open_list = Heap()

    head.gn=0
    head.calculate_hn(destination)
    head.calculate_fn()

    current_node = head
    step=1
    while(current_node != destination):
        #print(current_node)
        found_nodes = [x for x in current_node.find_neighbors(grid) if x.status != "found"]
        for node in found_nodes:
            node.status = "found"
            node.gn = step
            node.calculate_hn(destination)
            node.calculate_fn()
            node.predecessor = current_node
            open_list.add(node)
        
        closed_list.append(current_node)
        current_node = open_list.remove_min()
        step+=1

    stack = Stack()
    if current_node == destination:
        stack.push(current_node)
        while(current_node != head):
            current_node = current_node.predecessor
            stack.push(current_node)

    return stack
           
pygame.init()
cell_size = 20
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size)) #origin top left corner
clock = pygame.time.Clock()

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
        grid[x][y] = Node(x,y)
        grid[x][y].draw_box()

main_game = GAME()
s=search_path(grid, main_game)

#test cases
'''
a=Node(5,6)
a.fn = 11
b=Node(6,6)
b.fn=12
c=Node(7,8)
c.fn=15
d=Node(2,3)
d.fn = 5

s=Stack()
h=Heap()
h.add(a)
h.add(b)
h.add(c)
h.add(d)

while (not h.is_empty()):
    s.push(h.remove_min())
    
while (not s.is_empty()):
    print(s.pop())

'''
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if main_game.update == 'stop' and event.key== pygame.K_SPACE:
                main_game.update = 'play'
        if event.type == SCREEN_UPDATE and main_game.update == 'play':
            while (not s.is_empty()):
                new_direction=s.pop().coordinates - main_game.snake.body[0].coordinates
                main_game.update_new(new_direction)
                print(main_game.snake.body[0])
                #main_game.collision(cell_number)

                main_game.draw_elements()
                pygame.time.wait(100)
                pygame.display.update()
            #if main_game.snake.movement == "eating":
            #   pygame.quit()
            #   sys.exit()
                    
        
            #if main_game.update == 'play' and event.key == pygame.K_UP:
            #   main_game.update_new(Vector2(0,-1))
            #if main_game.update == 'play' and event.key == pygame.K_DOWN:
            #   main_game.update_new(Vector2(0,1))
            #if main_game.update == 'play' and event.key == pygame.K_LEFT:
            #    main_game.update_new(Vector2(-1,0))
            #if main_game.update == 'play' and event.key == pygame.K_RIGHT:
            #    main_game.update_new(Vector2(1,0))
    
    main_game.draw_elements()
    pygame.time.wait(10)
    pygame.display.update()
