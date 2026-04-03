import time
#DFS_fringe
class Stack:
    def __init__(self):self.items = []
    def push(self,item,priority=0):self.items.append(item)
    def pop(self):return self.items.pop()
    def is_empty(self):return len(self.items) == 0
#BFS_fringe
class Queue:
    def __init__(self):self.items =[]
    def push(self,item,priority=0):self.items.insert(0,item)
    def pop(self):return self.items.pop()
    def is_empty(self):return len(self.items) == 0
#UCS_fringe (小顶堆)
class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.counter = 0
    def push(self,item,priority):  #优先级，计数器，节点
        self.counter +=1 #优先级相等时，哪种顺序都被允许，counter的存在单纯是让程序跑通
        self.heap.append((priority,self.counter,item))
        self.bubble_up(len(self.heap)-1)
    def pop(self):
        if self.is_empty():return None
        if len(self.heap) == 1:return self.heap.pop()[2]
        root_item = self.heap[0][2]
        self.heap[0] = self.heap.pop()
        self.bubble_down(0)
        return root_item
    def is_empty(self):return len(self.heap) == 0
    def bubble_up(self,index):
        while index > 0:
            parent = (index-1)//2
            if self.heap[index][0]<self.heap[parent][0]:
                self.heap[index],self.heap[parent]=self.heap[parent],self.heap[index]
                index = parent
            else:
                break
    def bubble_down(self,index):
        size = len(self.heap)
        while True:
            smallest = index
            left,right = 2*index+1,2*index+2
            if left<size and self.heap[left][0]<self.heap[smallest][0]:
                smallest = left
            if right<size and self.heap[right][0]<self.heap[smallest][0]:
                smallest = right
            if smallest!=index:
                self.heap[index],self.heap[smallest] = self.heap[smallest],self.heap[index]
                index = smallest
            else:
                break

