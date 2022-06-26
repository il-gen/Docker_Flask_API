#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 11:55:57 2022

@author: growth358
"""

from datetime import datetime
import json


# A Linked List Node
class Node:
    def __init__(self, **kwargs):
        self.data=kwargs
        self.id = kwargs.get('id', None)
        self.created_at = datetime.strptime(kwargs.get('created_at', None), '%Y-%m-%dT%H:%M:%S.%f')
        self.next = None


# A Linked List class with a single head node
class LinkedList:
    def __init__(self):  
        self.head = None
  
  # insertion method for the linked list
    def insert(self, **kwargs):
        newNode = Node(**kwargs)
        if(self.head):
            current = self.head
            while(current.next):
                current = current.next
            current.next = newNode
        else:
            self.head = newNode
  
  # print method for the linked list
    def printLL(self):
        current = self.head
        while(current):
            print(current.data)
            current = current.next
        
      
class mergeSort:     
    
    def __init__(self):
        self.ll=[]
        
        
    # Get two list which their members sorted  by created_at (also id) attribute in ascending order
    # Merge this lists into one list which its member also sorted  by created_at attribute in ascending order
    def sortedMerge(self, a, b):
     
        # base cases
        if a is None:
            return b
        elif b is None:
            return a
     
        # pick either `a` or `b`, and recur
        if a.created_at < b.created_at:
            result = a
            result.next = self.sortedMerge(a.next, b)
        elif a.created_at > b.created_at:
            result = b
            result.next = self.sortedMerge(a, b.next)
        elif a.id <= b.id:
            result = a
            result.next = self.sortedMerge(a.next, b)
        else:
            result = b
            result.next = self.sortedMerge(a, b.next)
        return result
     
     
     
    # Merge mmembers of list_of_posts 
    # It takes a lists members of main list and generates the sorted Linklist  by created_at (& id) attribute in ascending order
    def mergeKLists(self, lists):
     
        # base
        if not lists:
            return None
     
        last = len(lists) - 1
     
        # repeat until only one list is left
        while last:
            (i, j) = (0, last)
     
            
            while i < j:
                # merge lists
                lists[i] = self.sortedMerge(lists[i], lists[j])
     
                # Get the next pair
                i = i + 1
                j = j - 1
     
                # if all pairs are merged, update last
                if i >= j:
                    last = j
     
        return lists[0]
    
    #Get Linklist which is sorted by created_at attribute in ascending order
    #Convert it into standard list which is sorted by created_at (& id) attribute in descending order
    #Used recursive method
    def makeMList(self,head):
        if head == None:
            return
        else:
            self.makeMList(head.next)
            self.ll.append(head.data)
