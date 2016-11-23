from time import time
from array import *
from copy import deepcopy

def makeEdgeWeightMatrixAndFlowList(file):
    global N
    firstLine = file.readline().split(",")
    N, start, end = int(firstLine[0].strip()), int(firstLine[1].strip()), int(firstLine[2].strip())

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
    Paths = newIntegerGraph(N, [])

    #make local copy of edges because it will change throughout the algorithm (want to keep original)
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

def GetEdgeLoads(originalEdgeWeights, minPaths, Flows):

    Loads = newIntegerGraph(N, 0)

    #using the flow for each edge pair, calculate individual edge Loads.
    for i in range(0, N):
        for j in range(0, N):
            if (i+1, j+1) in Flows:
                #for each edge in the path, add the flow
                for k in range(0, len(minPaths[i][j]) - 1):
                    a = minPaths[i][j][k] - 1
                    b = minPaths[i][j][k+1] - 1
                    Loads[a][b] += Flows[(i+1, j+1)]
            if originalEdgeWeights[i][j] == -1:
                if Loads[i][j] != 0:
                    print("Load found for nonexistent edge! Details: ", i+1, ":", j+1, minPaths[i][j])
                Loads[i][j] = -1

    return Loads

def GetPathHopLengths(Paths):
    hops = newIntegerGraph(N, -1)
    
    for i in range(0, N):
        for j in range(0, N):
            hopCount = len(Paths[i][j])
            hops[i][j] = hopCount - 1
    return hops

# Print utility function
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

# Utility function for empty array list (for integers) or List of dynamic Lists (for paths)
def newIntegerGraph(size, default = -1):
    G = []
    for i in range(0, size):
        if default == []:
            row = []
            for j in range(0, size):
                row.append([])
            G.append(row)
        else:
            G.append(array('i', [default]*size))
            G[i][i] = 0
    return G

##### MAIN SECTION ############

input(" ")
t0 = time()
Data = open("Input6.txt")

EdgeWeights, Flows = makeEdgeWeightMatrixAndFlowList(Data)
Data.close()

MinWeightPaths = FloydWarshall(EdgeWeights)
MinWeightHops = GetPathHopLengths(MinWeightPaths)
Loads = GetEdgeLoads(EdgeWeights, MinWeightPaths, Flows)
MinFlowPaths = FloydWarshall(Loads)
MinFlowHops = GetPathHopLengths(MinFlowPaths)


print("Original Edge Weights: ", prettyMatrix(EdgeWeights, 3))
print("Minimum Paths by Edge Weight (Distance): ", prettyMatrix(MinWeightPaths))
print("Hops for these paths (number of edges): ", prettyMatrix(MinWeightHops, 2))
print("Edge Loads: ", prettyMatrix(Loads, 5))
print("Minimum Paths by Edge Loads (Traffic): ", prettyMatrix(MinFlowPaths))
print("Hops for these paths (number of edges): ", prettyMatrix(MinFlowHops, 2))

t1= time()

print("Full time elapsed: ", t1-t0)

