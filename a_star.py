import snake_pygame

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

    def parent(self,j):
        return (j-1)//2

    def left(self,j):
        return 2*j+1

    def right(self,j):
        return 2*j+2

    def has_left(self,j):
        return self.left(j) <= len(self)

    def has_right(self,j):
        return self.right(j) <= len(self)

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

    def remove_min(self,node):
        self.swap(0, len(self.data)-1)
        self.data.pop(-1)
        self.downheap(0)
        
            
