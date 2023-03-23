import os
from PIL import Image, ImageDraw
import pandas as pd
images = []

#-Open the maze file and output a numpy array... returns numpy array
def OpenMaze(filename):
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
def ScanMaze(maze):
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

#-Simplify maze.. returns simplified maze array with only 0's, 1's, 2's, and 3's (0 = open, 1 = wall, 2 = start, 3 = goal)
def SimplifyMaze(maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'P':
                maze[i][j] = 0
            if maze[i][j] == '.':
                maze[i][j] = 0
            if maze[i][j] == '%':
                maze[i][j] = 1
            if maze[i][j] == ' ':
                maze[i][j] = 0
    return maze

#-Check the surrounding 'nodes', 
def MakeStep(k, maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == k:
                if i>0 and maze[i-1][j] == 0 and a[i-1][j] == 0:
                    maze[i-1][j] = k + 1
                if j>0 and maze[i][j-1] == 0 and a[i][j-1] == 0:
                    maze[i][j-1] = k + 1
                if i<len(maze)-1 and maze[i+1][j] == 0 and a[i+1][j] == 0:
                    maze[i+1][j] = k + 1
                if j<len(maze[i])-1 and maze[i][j+1] == 0 and a[i][j+1] == 0:
                    maze[i][j+1] = k + 1


def DrawMatrix(a,maze, thePath = []):
    #-Perform setup for graphical display of maze
    zoom = 15
    borders = 4
    im = Image.new('RGB', (zoom * len(a[0]), zoom * len(a)), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    for i in range(len(a)):
        for j in range(len(a[i])):
            color = (255, 255, 255) #-Color for wall
            r = 0
            if a[i][j] == 1:
                color = (0, 0, 0) #-Color for open area
            if i == start[0] and j == start[1]:
                color = (0, 0, 255) #-Color for start
                r = borders
            if i == end[0] and j == end[1]:
                color = (255, 0, 0) #-Color for goal
                r = borders
            draw.rectangle((j*zoom+r, i*zoom+r, j*zoom+zoom-r-1, i*zoom+zoom-r-1), fill=color)
            if maze[i][j] > 0:
                r = borders
                draw.ellipse((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1),
                               fill=(0,0,255))
    for l in range(len(thePath)-1):
        x = thePath[l][1]*zoom + int(zoom/2)
        y = thePath[l][0]*zoom + int(zoom/2)
        x1 = thePath[l+1][1]*zoom + int(zoom/2)
        y1 = thePath[l+1][0]*zoom + int(zoom/2)
        draw.line((x,y,x1,y1), fill=(255, 0, 0), width=3) #Color and width of connecting line
    draw.rectangle((0, 0, zoom * len(a[0]), zoom * len(a)), outline=(0,255,255), width=2) #-Color and size of border
    images.append(im)

#-Take input from user for maze file name
def getMazeFileName():
    mazeFile = input("Enter the name of the maze file: ")
    return 'Maze/'+mazeFile+'.lay'

def StartAnalysis():
    nodesExpanded = 0

    #-Create an empty matrix to store the path
    maze = []
    for i in range(len(a)):
        maze.append([])
        for j in range(len(a[i])):
            maze[-1].append(0)
            nodesExpanded += 1

    #-Save the start point, initialize counter variable (k)
    i,j = start
    maze[i][j] = 1
    k = 0
    maxDepth = 0

    #-Makes steps, until it reaches the end. Then it draws the current state of the matrix
    while maze[end[0]][end[1]] == 0:
        k += 1
        MakeStep(k, maze)
        DrawMatrix(a, maze)
        if k > maxDepth:
            maxDepth = k

    #-Save the end point, initialize counter variable (k)
    i, j = end
    k = maze[i][j]

    #-Traverse the matrix to find the shortest path (BFS)
    maze, thePath, maxDepth = BFS(maze, i, j, k, maxDepth)
    
    return maze, thePath, nodesExpanded, maxDepth

#-Traverse the matrix to find the shortest path (BFS)
def BFS(maze, i, j, k, maxDepth):
    thePath = [(i,j)]
    while k > 1:
        if i > 0 and maze[i-1][j] == k-1:
            i, j = i-1, j
            thePath.append((i, j))
            k -= 1
        elif j > 0 and maze[i][j-1] == k-1:
            i, j = i, j-1
            thePath.append((i, j))
            k -= 1
        elif i < len(maze)-1 and maze[i+1][j] == k-1:
            i, j = i+1, j
            thePath.append((i, j))
            k -= 1
        elif j < len(maze[i])-1 and maze[i][j+1] == k-1:
            i, j = i, j+1
            thePath.append((i, j))
            k -= 1
        DrawMatrix(a, maze, thePath)

        if maxDepth < len(thePath):
            maxDepth = len(thePath)
    return maze, thePath, maxDepth


mazeFile = getMazeFileName()
print(mazeFile)

#-Open the maze file(s) and perform setup
a = OpenMaze(mazeFile)
mazeData = ScanMaze(a)
a = SimplifyMaze(a)
start = mazeData[0]
end = mazeData[1]

#-Performs the BFS algorithm
maze, thePath, nodesExpanded, maxDepth = StartAnalysis()

#-Creates the flashing on the path (in the gif)
for i in range(20):
    if i % 2 == 0:
        DrawMatrix(a, maze, thePath)
    else:
        DrawMatrix(a, maze)


#-Print the path, number of nodes expanded, path cost, max tree depth, and max fringe size
print("Here is the path from start to end: ")
print(thePath)

print("Here is the number of nodes expanded: ", nodesExpanded)

print("Here is the path cost: ", len(thePath)-1)

print("Here is the maximum tree depth searched: ", maxDepth)

print("Here is the maximum size of the fringe: ", len(a))

#-Output the maze as a GIF animation
images[0].save(mazeFile[5:-4]+'.gif',
               save_all=True, append_images=images[1:],
               optimize=False, duration=1, loop=0)
