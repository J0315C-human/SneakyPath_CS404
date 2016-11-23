from array import *
from copy import deepcopy

def makeEdgeWeightMatrixAndFlowList(file):
    global N
    firstLine = file.readline().split(",")
    N, start, end = int(firstLine[0].strip()), int(firstLine[1].strip()), int(firstLine[2].strip())
    print(N, start, end)

    Matrix = newIntegerGraph(N)
    Flows = dict()

    for L in file:
        L = L.strip()
        if L != "":
            items = L.split(",")
            type = items[0].strip()
            from_node = int(items[1].strip())
            to_node =  int(items[2].strip())
            quantity = int( items[3].strip())
            if type == "E":
                Matrix[from_node-1][to_node-1] = quantity
            elif type == "F":
                Flows[(from_node, to_node)] = quantity
    return Matrix, Flows


def FloydWarshall(edgeMatrix):
    #initialize empty array 
    Paths = []
    for i in range(0, N):
        row = []
        for j in range(0, N):
            row.append([])
        Paths.append(row)

    #make a copy of edges because it will change throughout the algorithm (want to keep original)
    E = deepcopy(edgeMatrix)
    #for each > = zero degree edge, add path [a, b] to pathMatrix
    for a in range(0, N):
        for b in range(0, N):
            if (E[a][b] >= 0):
                Paths[a][b].append(a+1)
                if a != b:
                    Paths[a][b].append(b+1)

    #for each inclusion-candidate node D...
    for D in range(0, N):
        #go through and change matrix:
        #(Don't do this on any paths from a to D or D to b)
        operatingEdges = [f for f in range(0, N) if f != D]
        for a in operatingEdges:
            
            for b in operatingEdges:
                
                #- if path between a and b can be improved by going through n, update the spot
                #- skip the case where the path with node D included is infinity (using -1 as infinity)
                if not (a == b or E[a][D] == -1 or E[D][b] == -1):
                    withNode = E[a][D] + E[D][b]
                    if (E[a][b] > withNode) or (E[a][b] == -1):
                        E[a][b] = withNode
                        #-update path for a:b, using saved values for a:D, and D:b
                        Paths[a][b] = Paths[a][D][:-1] + Paths[D][b] 
          #move on to next D (inclusion-candidate node)

    return Paths

def GetEdgeFlows(minPaths, Flows):

    EdgeFlows = newIntegerGraph(N, -1)

    for i in range(0, N):
        for j in range(0, N):
            for p in range(0, len(minPaths[i][j])):
                #Go between each set of two nodes for the path
            if (i+1, j+1) in Flows:
                if EdgeFlows[i][j] == -1:
                    EdgeFlows[i][j] = Flows[(i+1, j+1)]
                else:
                    EdgeFlows[i][j] += Flows[(i+1, j+1)]

    return EdgeFlows

def GetPathHopLengths(Paths):
    hops = newIntegerGraph(N, 0)
    
    for i in range(0, N):
        for j in range(0, N):
            hopCount = len(Paths[i][j])
            if hopCount > 0:
                hops[i][j] = hopCount - 1
    return hops

def prettyMatrix(M, colWidth = 15):
    s = "\n"
    for i in range(0, N):
        line = []
        for j in range(0, N):
            if M[i][j] == -1:
                line.append("-")
            else:
                line.append(str(M[i][j]))
        s += (("{: >"+ str(colWidth)+"}") * N).format(*line) + "\n"
    return s

def newIntegerGraph(size, default = -1):
    G = []
    for i in range(0, size):
        G.append(array('i', [default]*size))
        G[i][i] = 0
    return G

##### MAIN SECTION ############
from time import time

input(" ")
t0 = time()
Data = open("TestInput.txt")

EdgeWeights, Flows = makeEdgeWeightMatrixAndFlowList(Data)
Data.close()
print(Flows)

MinWeightPaths = FloydWarshall(EdgeWeights)
MinWeightHops = GetPathHopLengths(MinWeightPaths)
EdgeFlows = GetEdgeFlows(MinWeightPaths, Flows)




print("Original Edge Weights: ", prettyMatrix(EdgeWeights, 5))
print("Minimum Paths: ",prettyMatrix(MinWeightPaths))
print("Minimum Path Hops (number of edges): ", prettyMatrix(MinWeightHops, 5))
print("Minimum Path Hops (number of edges): ", prettyMatrix(EdgeFlows, 5))

#==== Now go on and find Flow amounts for each Edge, using Flows.

t1= time()

print("Full time elapsed: ", t1-t0)

