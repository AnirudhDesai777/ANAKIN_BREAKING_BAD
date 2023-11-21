'''Helper functions for the grid environment, Q-learning and NLP'''

# we check all the valid neighbours of the current position for BFS
def validNeighbourBFS(Grid, node):
    neighbors = []
    
    if node[0]+1 >= 0 and node[0]+1 < len(Grid) and Grid[node] != -1:
        neighbors.append((node[0]+1, node[1]))
    if node[0]-1 >= 0 and node[0]-1 < len(Grid) and Grid[node] != -1:
        neighbors.append((node[0]-1, node[1]))    
    if node[1]+1 >= 0 and node[1]+1 < len(Grid) and Grid[node] != -1:
        neighbors.append((node[0], node[1]+1))
    if node[1]-1 >= 0 and node[1]-1 < len(Grid) and Grid[node] != -1:
        neighbors.append((node[0], node[1]-1))
    
    return neighbors

def validMovesASTAR(Grid, node,dark_goal):
    neighbors = []
    
    if node[0]+1 >= 0 and node[0]+1 < len(Grid) and Grid[node] != -1 and node!=dark_goal:
        neighbors.append((node[0]+1, node[1]))
    if node[0]-1 >= 0 and node[0]-1 < len(Grid) and Grid[node] != -1 and node!=dark_goal:
        neighbors.append((node[0]-1, node[1]))    
    if node[1]+1 >= 0 and node[1]+1 < len(Grid) and Grid[node] != -1 and node!=dark_goal:
        neighbors.append((node[0], node[1]+1))
    if node[1]-1 >= 0 and node[1]-1 < len(Grid) and Grid[node] != -1 and node!=dark_goal:
        neighbors.append((node[0], node[1]-1))
    
    return neighbors



	
	
	