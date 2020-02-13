#import json
#import os
#import random
import numpy as np

from Snake import Snake
from Board import Board


class Direction():
    """class providing outcomes of any given direction our snake may travel in """
    
    def __init__(self, vectorI, vectorJ, boardData):
        self.i=vectorI
        self.j=vectorJ
        self.s=Snake(boardData)
        self.b=Board(boardData)
        self.turn=boardData['turn']
        self.opponents = boardData['board']['snakes']
        
    def collideWall(self):
        """

        Returns
        -------
        bool
            whether direction results in collision with a wall.

        """
        x = self.s.headX
        y = self.s.headY
        if(x+self.i==-1 or x+self.i==self.b.width):
            return True
        elif(y+self.j==-1 or y+self.j==self.b.height):
            return True
        return False
    
    def collideSelf(self):
        """

        Returns
        -------
        bool
            whether direction results in collision with our neck.

        """

        if self.turn >= 1: #no neck on the first turn
            if(self.s.headX+self.i==self.s.neckX) & (self.s.headY+self.j==self.s.neckY):
                return True
        return False
    
    def collideOpponent(self):
        """

        Returns
        -------
        bool
            whether direction results in collision with rival snake

        """
        #TODO add cells surrounding opponent's head to forbidden list
        #TODO allow eating opponent's neck
        
        forbidden = []
        for snake in self.opponents:
            for pos in snake['body']:
                forbidden.append((pos['x'],pos['y']))
        nextPos = (self.s.headX+self.i,self.s.headY+self.j)
        if(nextPos in forbidden):
            return True
        
        return False
    
    def numOpponents():
        """returns the number of opponent snakes in a given direction"""
        #TODO
        
        return 0
    
    def numBody(self):
        """
        
        Returns
        -------
        int
            Number of body tiles in given direction
        int
            Minimum number of turns to any body tile in given direction

        """
        bodyCount=0
        nTurns = []
        for snake in self.b.snakes:
            for tile in snake['body']:
                if(self.i < 0): #moving left 
                    if(tile['x']<self.s.headX):
                        bodyCount += 1
                        nTurns.append(abs(self.s.headX-tile['x'])+abs(self.s.headY-tile['y']))
                    space = (self.s.headX)*(self.b.height)
                elif(self.i > 0): #moving right
                    if(tile['x']>self.s.headX):
                        bodyCount += 1
                        nTurns.append(abs(self.s.headX-tile['x'])+abs(self.s.headY-tile['y']))
                    space = (self.b.width-self.s.headX-1)*(self.b.height)
                elif(self.j > 0): #moving down
                    if(tile['y']>self.s.headY):
                        bodyCount += 1
                        nTurns.append(abs(self.s.headX-tile['x'])+abs(self.s.headY-tile['y']))
                    space = (self.b.height-self.s.headY-1)*(self.b.width)
                elif(self.j < 0): #moving up
                    if(tile['y']<self.s.headY):
                        bodyCount += 1
                        nTurns.append(abs(self.s.headX-tile['x'])+abs(self.s.headY-tile['y']))
                    space = (self.s.headY)*(self.b.width)
        density = bodyCount/space
        if(len(nTurns) > 0):
            minim = min(nTurns)
            mean = np.mean(nTurns)
        else:
            minim = 0
            mean = self.b.height+self.b.width
        return density,minim,mean
    
    def numFood(self):
        """
        
        Returns
        -------
        int
            Density of food sources in given direction
        int
            Minimum number of turns to any food in given direction
        int
            Average number of turns to food in given direction

        """
        foodCount=0
        nTurns = []
        for food in self.b.foodSources:
            if(self.i < 0): #moving left 
                if(food['x']<self.s.headX):
                    foodCount += 1
                    nTurns.append(abs(self.s.headX-food['x'])+abs(self.s.headY-food['y']))
                space = (self.s.headX)*(self.b.height)
            elif(self.i > 0): #moving right
                if(food['x']>self.s.headX):
                    foodCount += 1
                    nTurns.append(abs(self.s.headX-food['x'])+abs(self.s.headY-food['y']))
                space = (self.b.width-self.s.headX-1)*(self.b.height)
            elif(self.j > 0): #moving down
                if(food['y']>self.s.headY):
                    foodCount += 1
                    nTurns.append(abs(self.s.headX-food['x'])+abs(self.s.headY-food['y']))
                space = (self.b.height-self.s.headY-1)*(self.b.width)
            elif(self.j < 0): #moving up
                if(food['y']<self.s.headY):
                    foodCount += 1
                    nTurns.append(abs(self.s.headX-food['x'])+abs(self.s.headY-food['y']))
                space = (self.s.headY)*(self.b.width)
        density = foodCount/space
        if(len(nTurns) > 0):
            minim = min(nTurns)
            mean = np.mean(nTurns)
        else:
            minim = self.b.height+self.b.width
            mean = self.b.height+self.b.width
        return density,minim,mean


    def getReward(self):
        """returns reward (benefit of travel) for given direction"""
        if(self.collideWall() or self.collideSelf() or self.collideOpponent()):
            reward = -999
        else:
            reward = (0.2*self.numFood()[0]+                            # food density
                0.4*(1-self.numFood()[1]/(self.b.width+self.b.height))+ # min turns to food
                0.2*(1-self.numFood()[2]/(self.b.width+self.b.height))+ # mean turns to food
                0.1*-self.numBody()[0]+                                 # body density
                0.1*-(1-self.numBody()[1]/(self.b.width+self.b.height)))# min turns to body
            
            #logging
            print('On turn {0}, rewards for direction ({1},{2}) were:'.format(self.turn,self.i,self.j))
            print('food density: ',0.2*self.numFood()[0])
            print('food min t: ',0.4*(1-self.numFood()[1]/(self.b.width+self.b.height)))
            print('food mean t:',0.2*(1-self.numFood()[2]/(self.b.width+self.b.height)))
            print('body density: ',0.1*-self.numBody()[0])
            print('min turns to body: ',0.1*(self.numBody()[1]/(self.b.width+self.b.height)))
        return reward
    