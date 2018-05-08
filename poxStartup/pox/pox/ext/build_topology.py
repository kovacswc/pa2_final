import os
import sys
import numpy as np
import random
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.node import OVSController
from mininet.node import Controller
from mininet.node import RemoteController
from mininet.cli import CLI
sys.path.append("../../")
from pox.ext.jelly_pox import JELLYPOX
from subprocess import Popen
from time import sleep, time
from itertools import combinations
from mininet.log import setLogLevel
from mininet.util import dumpNodeConnections

from pox.openflow.discovery import Discovery 
import signal

def random_combination(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.sample(xrange(n),r))
    return tuple(pool[i] for i in indices)

class JellyFishTop(Topo):
    ''' TODO, build your topology here'''
    def build(self):
        
        switchList = []
        hostList = []
        numSwitches = 200
        numServerPerSwitch = 4
        numConnPerSwitch = 10
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
                hostList.append(self.addHost(hostName, ip = hostIP))
                self.addLink(switchList[-1],hostList[-1],port1=j)
                print "("+switchList[-1]+" ,"+hostList[-1]+")"
    #            f.write("self.addHost("+ hostName+")\n")
     #           f2.write("h,"+hostName+"\n")
      #          f.write("self.addLink("+ switchList[-1]+","+hostList[-1]+")\n")
       #         f2.write("l,"+switchList[-1]+","+hostList[-1]+","+str(j)+","+str(i)+"\n")
                 
        orderSwitch = range(numSwitches)
        np.random.shuffle(orderSwitch)
        count = np.zeros(numSwitches)

        for i in range(numSwitches-1):
           self.addLink(switchList[i],switchList[i+1])
           print "("+switchList[i]+" ,"+switchList[i+1]+")"
    #             
             f.write("self.addLink("+ switchList[i]+","+switchList[i+1]+")\n")
                 
        #self.addLink(switchList[0],switchList[2])


        # randGraph = nx.Graph()
        # numPortOnSwitch = [[0 for x in range(numConnPerSwitch)] for y in range(numConnPerSwitch)]
        # chooseS = range(numSwitches)
        # count = 0
        # while len(chooseS) > 1:
        #     (s1, s2) = random.sample(chooseS,2)
        #     if randGraph.has_edge(s1,s2):
        #         count += 1
        #         if count > 50:
        #             break
        #         continue
        #     count = 0
        #     numPortOnSwitch[s1] -= 1
        #     numPortOnSwitch[s2] -= 1
        #     if numPortOnSwitch[s1] == 0:
        #         chooseS.remove(s1)
        #     if numPortOnSwitch[s2] == 0:
        #         chooseS.remove(s2)
        #     self.addLink(switchList[s1],switchList[s2])
        # for combo in combinations(orderSwitch,2):
        #     #self.addLink(combo[0],combo[1])
        #     c0 = combo[0]
        #     c1 = combo[1]
        #     if(count[c0] < numConnPerSwitch and count[c1] < numConnPerSwitch):
        #         count[c0] += 1
        #         count[c1] += 1
        #         #print "("+str(c0)+" ,"+str(c1)+")"
        #         print "("+switchList[c0]+" ,"+switchList[c1]+")"
                
        #         self.addLink(switchList[c0],switchList[c1])
            
            # leftHost = self.addHost( 'h1' )
            # rightHost = self.addHost( 'h2' )
            # leftSwitch = self.addSwitch( 's3' )
            # rightSwitch = self.addSwitch( 's4' )

            # # Add links
            # self.addLink( leftHost, leftSwitch )
            # self.addLink( leftSwitch, rightSwitch )
            # self.addLink( rightSwitch, rightHost )


def experiment(net):
        net.start()
        sleep(5)
        print "iperf"
        net.iperf()

        h_0_0 = net.getNodeByName('h_0_0')
        print h_0_0.IP()
        #print "ping"
        #net.pingAll()
        
        net.stop()

def main():
	topo = JellyFishTop()

        #pox_arguments = '../../pox.py pox.ext.jellyfish_controller openflow.discovery'
        pox_arguments = ['../../pox.py', 'ext.jelly_controller','openflow.discovery']
        with open(os.devnull, "w") as fnull:
            pox_process = Popen(pox_arguments, stdout=fnull, stderr=fnull, shell=False, close_fds=True)
            # Allow time for the log file to be generated
            sleep(1)
        
        net = Mininet(topo=topo, host=CPULimitedHost, link = TCLink, controller=RemoteController)
        net.addController('pox', RemoteController, ip = '127.0.0.1', port = 6633)
	experiment(net)
        pox_process.send_signal(signal.SIGINT)

if __name__ == "__main__":
#    setLogLevel('info')
    main()

