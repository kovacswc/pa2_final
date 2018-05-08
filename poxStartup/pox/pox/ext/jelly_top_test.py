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
    print macAddr
    return macAddr

class JellyFishTop(Topo):
    ''' TODO, build your topology here'''
    def build(self):
        
        switchList = []
        hostList = []
        numSwitches = 100
        numServerPerSwitch = 2
        numConnPerSwitch = 8
#        f = open('curTop','w')
 #       f2 = open('curTopMap','w')
        for i in range(1, numSwitches+1):
            switchName = 's'+str(i)
            switchList.append(self.addSwitch(switchName))
  #          f.write("self.addSwitch("+ switchName+")\n")
   #         f2.write("s,"+switchName+"\n")
            for j in range(1, numServerPerSwitch+1):
                hostName = 'h_'+str(i)+'_'+str(j)
                
                hostIp = "10."+str(i)+"."+str(j)+".1"
                hostList.append(self.addHost(hostName, ip = hostIp, mac = ip_to_mac(hostIp)))
                self.addLink(switchList[-1],hostList[-1],port1=j)
                print "("+switchList[-1]+" ,"+hostList[-1]+")"
    #            f.write("self.addHost("+ hostName+")\n")
     #           f2.write("h,"+hostName+"\n")
      #          f.write("self.addLink("+ switchList[-1]+","+hostList[-1]+")\n")
       #         f2.write("l,"+switchList[-1]+","+hostList[-1]+","+str(j)+","+str(i)+"\n")
                 
        orderSwitch = range(numSwitches)
        np.random.shuffle(orderSwitch)
        count = np.zeros(numSwitches)

        #Linear
        # for i in range(numSwitches-1):
        #    self.addLink(switchList[i],switchList[i+1])
        #    print "("+switchList[i]+" ,"+switchList[i+1]+")"
        #Add cycle to linear
        # self.addLink(switchList[0],switchList[3])

        #Jelly
        randGraph = nx.Graph()
        numPortOnSwitch = [numConnPerSwitch for x in range(numSwitches)]
        chooseS = range(numSwitches)
        count = 0
        while len(chooseS) > 1:
            (s1, s2) = random.sample(chooseS,2)
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
