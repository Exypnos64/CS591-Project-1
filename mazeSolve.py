from PIL import Image, ImageDraw
import pandas as pd
# import numpy as np
from collections import deque
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
    except FileNotFoundError:
        print(f"File {filename} not found")
        exit()
    return data

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

#-Add a manhattan distance heuristic
def ManhattanDistance(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

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
# k:            a counter for the amount of nodes we have encountered
# maze:         array of 0s and 1s: 1s are walls and 0s are spaces
def aStarAlgorithm(maze, a, start, end):
    open = []
    closed = []
    # push start node
    open.append([start[0],start[1], 0, 0, 0])
    #print(end)

    maxDepth = 0
    nodesExpanded = 0
    fringe = len(open)

    # while open has something in it
    while(open):
        # get minimum f value (g + h) and remove from list
        q = min(open, key=lambda x: x[2] + x[3])
        open.remove(q)

        if q[4] > maxDepth:
            maxDepth = q[4]
        
        nodesExpanded += 1

        #print('step:', k, 'at', (q[0]+1,q[1]+1))
        #print('f:', q[2]+q[3])
        maze[q[0]][q[1]] = nodesExpanded if nodesExpanded != 1 else -1

        successor = []
        
        # above
        successor.append([q[0]-1, q[1], q[2]+1, 0, q[4]+1])
        successor[0][3] = ManhattanDistance((successor[0][0], successor[0][1]), end)
        # left
        successor.append([q[0], q[1]-1, q[2]+1, 0, q[4]+1])
        successor[1][3] = ManhattanDistance((successor[1][0], successor[1][1]), end)
        # down
        successor.append([q[0]+1, q[1], q[2]+1, 0, q[4]+1])
        successor[2][3] = ManhattanDistance((successor[2][0], successor[2][1]), end)
        # right
        successor.append([q[0], q[1]+1, q[2]+1, 0, q[4]+1])
        successor[3][3] = ManhattanDistance((successor[3][0], successor[3][1]), end)

        endFound = False
        
        for node in successor:
            # if we found end goal
            if [node[0], node[1]] == end:
                maze[end[0]][end[1]] = 1
                q = node
                #print('end goal found')
                endFound = True
                break
            
            # If we find a wall
            if a[node[0]][node[1]] == 1:
                #print((node[0]+1,node[1]+1), 'is wall')
                continue

            # if location has been visited
            if (node[0], node[1]) in closed:
                #print((node[0]+1,node[1]+1), 'visited')
                continue

            # if we are already visiting a location
            if any(sublist[0] == node[0] and sublist[1] == node[1] for sublist in open):
                #print('visiting', (node[0]+1,node[1]+1))
                continue
            
            #print('appending', (node[0]+1,node[1]+1))
            open.append(node)

        closed.append((q[0], q[1]))
        DrawMatrix(a, maze, start, end)

        if len(open) > fringe:
            fringe = len(open)

        if endFound:
            if q[4] > maxDepth:
                maxDepth = q[4]
            return maxDepth, nodesExpanded, fringe
        #print()

def bfsAlgorithm(maze, a, start, end):
    open = deque()
    closed = []
    # push start node
    open.append([start[0],start[1], 0])
    #print(end)

    maxDepth = 0
    nodesExpanded = 0
    fringe = 1

    # while open has something in it
    while(open):
        q = open.popleft()

        if q[2] > maxDepth:
            maxDepth = q[2]
        
        nodesExpanded += 1

        #print('step:', k, 'at', (q[0]+1,q[1]+1))
        maze[q[0]][q[1]] = nodesExpanded if nodesExpanded != 1 else -1

        successor = []
        
        # above
        successor.append([q[0]-1, q[1], q[2]+1])
        # left
        successor.append([q[0], q[1]-1, q[2]+1])
        # down
        successor.append([q[0]+1, q[1], q[2]+1])
        # right
        successor.append([q[0], q[1]+1, q[2]+1])

        endFound = False
        
        for node in successor:
            # if we found end goal
            if [node[0], node[1]] == end:
                maze[end[0]][end[1]] = 1
                #print('end goal found')
                q = node
                endFound = True
                break
            
            # If we find a wall
            if a[node[0]][node[1]] == 1:
                #print((node[0]+1,node[1]+1), 'is wall')
                continue

            # if location has been visited
            if (node[0], node[1]) in closed:
                #print((node[0]+1,node[1]+1), 'visited')
                continue

            # if we are already visiting a location
            if any(sublist[0] == node[0] and sublist[1] == node[1] for sublist in open):
                #print('visiting', (node[0]+1,node[1]+1))
                continue
            
            #print('appending', (node[0]+1,node[1]+1))
            open.append(node)

        closed.append((q[0], q[1]))
        DrawMatrix(a, maze, start, end)

        if len(open) > fringe:
            fringe = len(open)

        if endFound:
            if q[2] > maxDepth:
                maxDepth = q[2]
            return maxDepth, nodesExpanded, fringe
        #print()

def DrawMatrix(a, maze, start, end, thePath = []):
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
def getMazeFileName(mazeFile = ''):
    if mazeFile == '':
        mazeFile = input("Enter the name of the maze file: ")
    return 'Maze/'+mazeFile+'.lay'

def analysis(a, start, end, algorithm = ''):
    #-Create an empty matrix to store the path
    maze = []
    for i in range(len(a)):
        maze.append([])
        for j in range(len(a[i])):
            maze[i].append(0)

    #-Save the start point, initialize counter variable (k)
    i,j = start
    maze[i][j] = -1

    #-Makes steps, until it reaches the end. Then it draws the current state of the matrix
    if (algorithm.lower() == 'bfs'):
        maxDepth, nodesExpanded, fringe = bfsAlgorithm(maze, a, start, end)
    elif (algorithm.lower() == 'astar'):
        maxDepth, nodesExpanded, fringe = aStarAlgorithm(maze, a, start, end)
    

    #-Retrace our steps to redraw path to start
    maze, thePath = retraceSteps(a, maze, end, start, end)
    
    return maze, thePath, nodesExpanded, maxDepth, fringe

#-Retrace our steps to redraw path to start
# maze:     array of 0s and 1s: 1s are walls and 0s are spaces with step numbers inserted
# cursor:   value we are looking at (starts at end)
# k:        the step value at the maze's endpoint
# maxDepth: the maximum depth we traversed
def retraceSteps(a, maze, cursor, start, end):
    thePath = [cursor]
    # print((cursor[0]+1, cursor[1]+1), maze[cursor[0]][cursor[1]], "\t", (start[0]+1, start[1]+1), maze[start[0]][start[1]])
    while cursor != start:
        # find the least number around us that is not 0
        coordPairs = [[cursor[0]-1, cursor[1]], [cursor[0], cursor[1]-1], [cursor[0]+1, cursor[1]], [cursor[0], cursor[1]+1]]
        cursor = min(coordPairs, key=lambda x: maze[x[0]][x[1]] if maze[x[0]][x[1]] != 0 and maze[x[0]][x[1]] != 1 else float('inf'))
        # print((cursor[0]+1, cursor[1]+1), maze[cursor[0]][cursor[1]])
        thePath.append(cursor)
        DrawMatrix(a, maze, start, end, thePath)

    thePath.reverse()
    return maze, thePath


def main(mazeFile = '', algorithm = ''):
    print(f'\n--- {algorithm} Algorithm {mazeFile} ---')
    mazeFile = getMazeFileName(mazeFile)

    #-Open the maze file(s) and perform setup
    a = OpenMaze(mazeFile)
    mazeData = ScanMaze(a)
    a = SimplifyMaze(a)
    start = mazeData[0]
    end = mazeData[1]

    #-Performs the aStar algorithm
    maze, thePath, nodesExpanded, maxDepth, fringe = analysis(a, start, end, algorithm)
    
    #-Creates the flashing on the path (in the gif)
    for i in range(20):
        if i % 2 == 0:
            DrawMatrix(a, maze, start, end, thePath)
        else:
            DrawMatrix(a, maze, start, end)


    #-Print the path, number of nodes expanded, path cost, max tree depth, and max fringe size
    print("Here is the path from start to end: ")
    print(thePath)
    print("Here is the number of nodes expanded: ", nodesExpanded)
    print("Here is the path cost: ", len(thePath)-1)
    print("Here is the maximum tree depth searched: ", maxDepth)
    print("Here is the maximum size of the fringe: ", fringe)

    #-Output the maze as a GIF animation
    images[0].save(mazeFile[5:-4]+f'-{algorithm.upper()}.gif',
                save_all=True, append_images=images[1:],
                optimize=False, duration=1, loop=0)
    

if __name__ == '__main__':
    mazeFiles = ['smallMaze', 'mediumMaze', 'bigMaze', 'sampleMazeFile', 'openMaze']
    mazeFile = mazeFiles[0]

    # for mazeFile in mazeFiles:
    images = []
    main(mazeFile, 'bfs')
    images = []
    main(mazeFile, 'aStar')