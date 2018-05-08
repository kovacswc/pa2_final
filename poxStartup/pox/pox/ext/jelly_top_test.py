from mininet.topo import Topo
import numpy as np
import networkx as nx
import random

def random_combination(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.sample(xrange(n),r))
    return tuple(pool[i] for i in indices)

def ip_to_mac(ip):
    (nothing, sN, iPt, nada) = ip.split(".")
    switch = int(sN)
    switchHex = hex(switch)[2:]
    port = int(iPt)
    portHex = hex(port)[2:]
    if len(switchHex) == 1:
        switchHex = "0"+switchHex
    if len(portHex) == 1:
        portHex = "0"+portHex
    macAddr = "00:00:00:00:"+switchHex+":"+portHex
    return macAddr

class JellyFishTop(Topo):
    ''' TODO, build your topology here'''
    def build(self):
        
        switchList = []
        hostList = []
        numSwitches = 100
        numServerPerSwitch = 2
        numConnPerSwitch = 8
        #Set up number of switches and hosts connected to each
        for i in range(1, numSwitches+1):
            switchName = 's'+str(i)
            switchList.append(self.addSwitch(switchName))
            for j in range(1, numServerPerSwitch+1):
                #Set host ip to include switch id and port info
                hostName = 'h_'+str(i)+'_'+str(j)                
                hostIp = "10."+str(i)+"."+str(j)+".1"
                hostList.append(self.addHost(hostName, ip = hostIp, mac = ip_to_mac(hostIp)))
                self.addLink(switchList[-1],hostList[-1],port1=j)
                 
        orderSwitch = range(numSwitches)
        np.random.shuffle(orderSwitch)
        count = np.zeros(numSwitches)

        #Jelly Connections
        randGraph = nx.Graph()
        numPortOnSwitch = [numConnPerSwitch for x in range(numSwitches)]
        chooseS = range(numSwitches)
        count = 0
        while len(chooseS) > 1:
            (s1, s2) = random.sample(chooseS,2)
            #Get out if can't find a final link
            if randGraph.has_edge(s1,s2):
                count += 1
                if count > 50:
                    break
                continue
            count = 0
            numPortOnSwitch[s1] -= 1
            numPortOnSwitch[s2] -= 1
            if numPortOnSwitch[s1] == 0:
                chooseS.remove(s1)
            if numPortOnSwitch[s2] == 0:
                chooseS.remove(s2)
            self.addLink(switchList[s1],switchList[s2])
            

           
topos = { 'mytopo': (lambda: JellyFishTop() ) }
