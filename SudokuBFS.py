import queue
from copy import deepcopy

#These are the grids which we will test
test1 = [[1,5,0,0,4,0],
         [2,4,0,0,5,6],
         [4,0,0,0,0,3],
         [0,0,0,0,0,4],
         [6,3,0,0,2,0],
         [0,2,0,0,3,1]]

test2 = [[0,0,0,0,4,0],
         [5,6,0,0,0,0],
         [3,0,2,6,5,4],
         [0,4,0,2,0,3],
         [4,0,0,0,6,5],
         [1,5,6,0,0,0]]

test3 = [[0,0,0,8,4,0,6,5,0],
         [0,8,0,0,0,0,0,0,9],
         [0,0,0,0,0,5,2,0,1],
         [0,3,4,0,7,0,5,0,6],
         [0,6,0,2,5,1,0,3,0],
         [5,0,9,0,6,0,7,2,0],
         [1,0,8,5,0,0,0,0,0],
         [6,0,0,0,0,0,0,4,0],
         [0,5,2,0,8,6,0,0,0]]


#This code checks to see whether or not we are done solving the puzzle
def goal_test(state):
    for i in range(0,len(state)):
        localCount = 0
        for j in range(0, len(state)):
            localCount += state[i][j]
        if(localCount != fact_sum(len(state))):
            return False
    ##Check the columns
    for i in range(0,len(state)):
        localCount = 0
        for j in range(0, len(state)):
            localCount += state[j][i]
        if(localCount != fact_sum(len(state))):
            return False
    ##Check for squares to be properly filled in
    if(len(state) == 6):
        for i in range(0,6,2):
            if(not checkGrid(state,i,0)): 
                return False  
            if(not checkGrid(state,i,3)):  
                return False            
    elif(len(state)==9):
        for horiz in range(0,3):
            for vert in range(0,3):
                localCount = 0
                for i in range(0,3):
                    for j in range(0,3):
                        localCount += state[(horiz*3)+i][(vert*3)+j]
                if(localCount != 45):
                    return False
    return True

def fact_sum(hold):
    returnInt = 0
    while(hold != 0):
        returnInt += hold
        hold = hold - 1
    return returnInt

def checkGrid(state, x, y):
    returnGrid = []
    returnGrid.append(state[x][y])
    returnGrid.append(state[x][y+1])
    returnGrid.append(state[x][y+2])
    returnGrid.append(state[x+1][y])
    returnGrid.append(state[x+1][y+1])
    returnGrid.append(state[x+1][y+2])
    return sum(returnGrid) == 21

def getValues(state):
	possibleValues=[]
	for i in range(0, len(state)):
		for j in range(0,len(state)):
			if(state[i][j] == 0):
				for k in range(1, len(state)+1):
					if(checkRow(state, i, k) and checkVertical(state, j, k)):
						possibleValues.append(k)
				return possibleValues
	return None

def checkVertical(state, column, value):
	for i in range(0,len(state)):
		if(state[i][column] == value):
			return False
	return True

def checkRow(state, row, value):
	if value in state[row]:
		return False
	return True


def createBoards(state, valueQueue):
	boards = []
	x = 0
	y = 0
	find = False
	for i in range(0, len(state)):
		for j in range(0,len(state)):
			if(state[i][j] == 0):
				x = i
				y = j
				find = True
				break
		if find:
			break
	for i in valueQueue:
		state[x][y] = i
		boards.append(deepcopy(state))
	return boards

class Node(object):
	def __init__(self, state, children):
		self.state = state
		self.children = []

	def appendChild(self, newState):
		self.children.append(newState)

	def getState(self):
		return self.state


def printNode(node):
	print("State: " + str(node.state))
	print("Children: " + str(node.children))
	print("-------------------------------")

def printBoard(state):
	for i in range(0,len(state)):
		print("\n")
		for j in range(0,len(state)):
			print(state[i][j], end="")
	print("\n___________________")

def breadth_first_search(state):
    # Check if current board meets Goal_Test criteria
    firstNode = Node(state, [])


    if goal_test(firstNode.state):
        return firstNode.state
    # Create a Queue to store all nodes of a particular level. Import QueueClass()
    frontier=queue.Queue()
    frontier.put(firstNode)

    # Loop until all nodes are explored(frontier queue is empty) or Goal_Test criteria are met
    while frontier:
        # Remove from frontier, for analysis
        localChild = frontier.get()
        localState = localChild.state
        
        possibleValues = getValues(localState)
        if (possibleValues == None):
        	print("No solution found")
        	return
        localChild.children = createBoards(localState, possibleValues)
        # Loop over all children of the current node
        # Note: We consider the fact that a node can have multiple child nodes here
        for child in localChild.children:
            # If child node meets Goal_Test criteria
            if goal_test(child):
                return child
            # Add every new child to the frontier
            frontier.put(Node(child,[]))
    return None
printBoard(breadth_first_search(test1))
printBoard(breadth_first_search(test2))
printBoard(breadth_first_search(test3))
