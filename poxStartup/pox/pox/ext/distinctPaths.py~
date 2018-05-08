import networkx as nx
import random
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from itertools import islice


def k_shortest_paths(G, source, target, k, weight = None):
    return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))
#98, 27
#180, 10, 5
numSwitches = 180
numPorts = 10
numHosts = 5

randGraph = nx.Graph()
adjMatrix = [[0 for x in range(numSwitches)] for y in range(numSwitches)]
numPortSwitches = [numPorts for x in range(numSwitches)]
totPairs = numSwitches * numPorts

#My naming scheme is pretty awful here, had a different idea in mind, that went
#to what is now, so ports don't quite align with what is going on
portsToChooseFrom = range(numSwitches)

print numPortSwitches
count = 0
while len(portsToChooseFrom) > 1:
    (port1, port2) = random.sample(portsToChooseFrom,2)

    if randGraph.has_edge(port1,port2):
        #print totPairs
        # print portsToChooseFrom
        # print "("+str(port1)+", "+str(port2)+")"
        # print numPortSwitches[port1]
        # print numPortSwitches[port2]
        # print randGraph.degree[port1]
        # print randGraph.degree[port2]
        count += 1
        if count > 50:
            print "Something went wrong!"
            break
        continue
    count = 0
    totPairs -= 2
#    print "("+str(port1)+", "+str(port2)+")"
    
    numPortSwitches[port1] -= 1
    numPortSwitches[port2] -= 1
    if numPortSwitches[port1] == 0:
        portsToChooseFrom.remove(port1)
    if numPortSwitches[port2] == 0:
        portsToChooseFrom.remove(port2)
    adjMatrix[port1][port2] = 1
    adjMatrix[port2][port1] = 1
    randGraph.add_edge(port1,port2)

print randGraph.number_of_edges()

drawFig = False

if drawFig:
    plt.subplot(121)
    nx.draw(randGraph, with_labels = True, font_weight='bold')
    plt.savefig("test.png")

#ecmp_8_counts = [[0 for x in range(numSwitches)] for y in range(numSwitches)]
#ecmp_64_counts = [[0 for x in range(numSwitches)] for y in range(numSwitches)]
#short_8_counts = [[0 for x in range(numSwitches)] for y in range(numSwitches)]
ecmp_8_counts = np.zeros((numSwitches, numSwitches))
ecmp_64_counts = np.zeros((numSwitches, numSwitches))

short_8_counts = np.zeros((numSwitches, numSwitches))

def update_count(path,updMatrix):
    for nodeInd in range(len(path)-1):
        node1 = path[nodeInd]
        node2 = path[nodeInd+1]
        updMatrix[node1][node2] += 1


hosts = np.arange(numHosts*numSwitches)
np.random.shuffle(hosts)
hostAssign = np.split(hosts, numSwitches)
        
receivers = range(numHosts*numSwitches)
pairs = []
hostSwitchPairs = {}
for switchNum in range(numSwitches):
    for host in hostAssign[switchNum]:
        hostSwitchPairs[host] = switchNum
        

for i in range(numHosts*numSwitches):
    pairSw = random.choice(receivers)
    while pairSw == i and hostSwitchPairs[i] != hostSwitchPairs[pairSw]:
        pairSw = random.choice(receivers)
    pairs.append((i,pairSw))
    receivers.remove(pairSw)

print "PAIR LENGTH: "

# for i in range(numSwitches):
#     for j in range(i+1, numSwitches):
#         pairs.append((i,j))
#         pairs.append((j,i))
        
print len(pairs)



for (i,j) in pairs:

    switchI = hostSwitchPairs[i]
    switchJ = hostSwitchPairs[j]
    
    shortest_paths = k_shortest_paths(randGraph, switchI, switchJ, 64)

    count = 0
    length = len(shortest_paths[0])
    
    for path in shortest_paths:
        
        count += 1
        if count <= 8:
            update_count(path,short_8_counts)
        if length == len(path) and count <= 8:
            update_count(path, ecmp_8_counts)
        if length == len(path) and count <= 64:
            update_count(path, ecmp_64_counts)
        if count > 64:
            break
        

print short_8_counts[0].max()
histVals = []
histVal_e8 = []
histVal_e64 = []

for i in range(numSwitches):
    for j in range(numSwitches):
        if short_8_counts[i][j] != 0:
            histVals.append(short_8_counts[i][j])
        if ecmp_8_counts[i][j] != 0:
            histVal_e8.append(ecmp_8_counts[i][j])
        if ecmp_64_counts[i][j] != 0:
            histVal_e64.append(ecmp_64_counts[i][j])
            
#print histVals
for i in range(len(histVals)-len(histVal_e8)):
    histVal_e8.append(0)
for i in range(len(histVals)-len(histVal_e64)):
    histVal_e64.append(0)
    
histVals = sorted(histVals)
histVal_e8 = sorted(histVal_e8)
histVal_e64 = sorted(histVal_e64)

plt.plot(histVals)
plt.plot(histVal_e8)
plt.plot(histVal_e64)
plt.xlabel("Link Rank")
plt.ylabel("# Distinct Paths on Link")
plt.savefig("hist.png")

