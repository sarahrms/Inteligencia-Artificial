class Graph():
    def __init__(self):
        self.graph = [] #list of edges

    def insertEdge(self, v1, v2, cost):
        if ((v1, v2, cost) in self.graph) | ((v2, v1, cost) in self.graph): #non directional
            print("Already exists")
        else:
            self.graph.append((v1, v2, cost)) #tuple

    def getEdges(self, v): #return a list with all the edges of that vertice
        list = []
        for l in self.graph:
            if (l[0] == v):
                list.append(l)
            if (l[1] == v):
                list.append((l[1],l[0],l[2])) #reverse order
        return list

    def print(self):
        print("Graph: ")
        for l in self.graph:
            print(l)

H = {'Arad': 366, 'Bucharest': 0, 'Craiova': 160,
     'Dobreta': 242, 'Eforie': 161, 'Fagaras': 176,
     'Giurgiu': 77, 'Hirsova': 151, 'Iasi': 226,
     'Lugoj': 244, 'Mehadia': 241, 'Neamt': 234,
     'Oradea': 380, 'Pitesti': 10, 'Rimnicu Vikea': 193,
     'Sibiu': 253, 'Timisoara': 329, 'Urziceni': 80,
     'Vaslui': 199, 'Zerind': 374}

G = Graph()
G.insertEdge('Arad', 'Timisoara', 118)
G.insertEdge('Arad', 'Zerind', 75)
G.insertEdge('Arad', 'Sibiu', 140)
G.insertEdge('Zerind','Oradea', 71)
G.insertEdge('Oradea','Sibiu', 151)
G.insertEdge('Sibiu','Fagaras', 99)
G.insertEdge('Sibiu','Rimnicu Vikea', 80)
G.insertEdge('Rimnicu Vikea','Pitesti', 97)
G.insertEdge('Rimnicu Vikea','Craiova', 146)
G.insertEdge('Craiova','Dobreta', 120)
G.insertEdge('Dobreta','Mehadia', 75)
G.insertEdge('Mehadia','Lugoj', 70)
G.insertEdge('Lugoj','Timisoara', 111)
G.insertEdge('Craiova','Pitesti', 138)
G.insertEdge('Pitesti','Bucharest', 101)
G.insertEdge('Fagaras','Bucharest', 211)
G.insertEdge('Bucharest','Giurgiu', 90)
G.insertEdge('Bucharest','Urziceni', 85)
G.insertEdge('Urziceni','Hirsova', 98)
G.insertEdge('Hirsova','Eforie', 86)
G.insertEdge('Urziceni','Vaslui', 142)
G.insertEdge('Vaslui','Iasi', 92)
G.insertEdge('Iasi','Neamt', 87)

startVertice = 'Lugoj'
objectiveVertice = 'Bucharest'

currentVertice = startVertice
currentPath = ([currentVertice], 0) #tuple with the list of vertices and the cost of the path

possiblePaths = [] #list of already calculated possible paths
checkedVertices = []# list of checked vertices

while currentVertice != objectiveVertice:
    print("----------------------------------------------------------------------------------------------------------------")
    print("Current vertice: ", end="")
    print(currentVertice)
    print("Current Path: ", end="")
    print(currentPath)

    edges = G.getEdges(currentVertice) #gets all the edges conected to that vertice, with the currentVertice in position [0]

    print("\nChecked Vertices: ", end="")
    print(checkedVertices)
    print("All Current Vertice Edges: ", end="")
    print(edges)

    for someEdge in edges:
        if someEdge[1] not in checkedVertices: #if that edge doesn lead to an already checked vertice
            path = list (currentPath[0]) #gets the list of vertices of current path
            path.append(someEdge[1]) #add the child to the path
            cost = currentPath[1] + someEdge[2] #gets the cost of the new path
            possiblePaths.append((path, cost)) #add the new possible path to the list

    checkedVertices.append(currentVertice) #now that weve got all the children, were done with this vertice

    print("\nPossible Paths: ", end="")
    print(possiblePaths)

    minorCost = 100000

    for somePath in possiblePaths:
        verticesList = list (somePath[0]) #gets the list of vertices of that path
        vertice = verticesList[len(verticesList)-1] #gets the last vertice of that list

        cost = (somePath[1]+ H[vertice]) #calculate the heuristic cost

        print("---Path: ", somePath, ", Heuristic: ", H[vertice], "Total Cost: ", cost)

        if minorCost > cost:
            chosenPath = somePath
            minorCost = cost #heuristic cost
            chosenVertice = vertice

    print('\nChosen Path: ', end="")
    print(chosenPath)
    print()

    currentPath = chosenPath
    currentVertice = chosenVertice
    possiblePaths.remove(chosenPath)


print("----------------------------------------------------------------------------------------------------------------")

print("\nFinal Path: ", end="")
print(currentPath)
















 # list de nodes that have ben checked
