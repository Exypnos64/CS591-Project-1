import pandas as pd
import numpy as np

#-Open the maze file and output a numpy array... returns numpy array
def openMaze(filename):
    try:
        #-create a dataframe representing the maze
        mazeDF = pd.read_csv(filename, names=['column'])
        #-split the dataframe into columns
        data = mazeDF['column'].str.split('', expand=True)
        #-remove the first and last column
        data = data.drop(data.columns[[0, len(data.columns)-1]], axis=1)
        #-convert the dataframe to a numpy array
        data = data.values
    except fileNotFoundException:
        print("File not found")
    return data;
    
#-Scan locations by searching down columns... returns array[start Location, goal Location, list of wall locations]
def scanMaze(maze):
    start = [0,0]
    goal = [0,0]
    wall = [0,0]
    wallList = []
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'P':
                start = [i,j]
            if maze[i][j] == '.':
                goal = [i,j]
            if maze[i][j] == '%':
                wall = [i,j]
                wallList.append(wall)
    return [start, goal, wallList]


maze = openMaze("maze.txt")

print(maze)
