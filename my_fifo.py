#!/usr/bin/env python

############################################
# this EMPTY python fifo class was written by dr fred depiero at cal poly
# distribution is unrestricted provided it is without charge and includes attribution

class my_fifo:
    '''Implements an array-based, efficient first-in first-out Abstract Data Type 
       using a Python array (faked using a List)'''

    def __init__(self, capacity):
        '''Creates an empty Queue with a capacity'''
        if type(capacity) != int:
            raise TypeError("Capacity given must be of type int")
        if capacity < 0:
            raise ValueError("Capacity must be a positive (zero-inclusive) value")
        self.array = [None] * capacity
        self.capacity = capacity
        self.num_items = 0
        self.back = 0
        self.front = 0

    def is_empty(self):
        '''Returns True if the Queue is empty, and False otherwise
           MUST have O(1) performance'''
        return (self.num_items == 0)

    def is_full(self):
        '''Returns True if the Queue is full, and False otherwise
           MUST have O(1) performance'''
        return (self.num_items == self.capacity)

    def enqueue(self, item):
        '''If Queue is not full, enqueues (adds) item to Queue 
           If Queue is full when enqueue is attempted, raises IndexError
           MUST have O(1) performance'''
        if self.is_full():
            raise IndexError("Cannot enqueue to a full queue")
        self.array[self.back] = item
        self.back += 1
        if self.back >= self.capacity: # wraparound
            self.back = 0
        self.num_items += 1

    def dequeue(self):
        '''If Queue is not empty, dequeues (removes) item from Queue and returns item.
           If Queue is empty when dequeue is attempted, raises IndexError
           MUST have O(1) performance'''
        if self.is_empty():
            raise IndexError("Cannot dequeue an empty queue")
        temp = self.array[self.front]
        self.front += 1
        if self.front >= self.capacity: # wraparound
            self.front = 0
        self.num_items -= 1
        return temp
        
    def size(self):
        '''Returns the number of elements currently in the Queue, not the capacity
           MUST have O(1) performance'''
        return self.num_items