# Copyright 2012 James McCauley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This component is for use with the OpenFlow tutorial.

It acts as a simple hub, but can be modified to act like an L2
learning switch.

It's roughly similar to the one Brandon Heller did for NOX.
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
import numpy as np
import networkx as nx
from collections import defaultdict
from random import randint
from pox.openflow.discovery import Discovery
from pox.lib.packet.arp import arp
from pox.lib.packet.ethernet import ethernet
from pox.lib.addresses import EthAddr

log = core.getLogger()

#def dpid_to_mac (dpid):
#  return EthAddr("%012x" % (dpid & 0xffFFffFFffFF,))

def ip_to_mac(ip):
    (nothing, sN, iPt, nada) = str(ip).split(".")
    switch = int(sN)
    switchHex = hex(switch)[2:]
    port = int(iPt)
    portHex = hex(port)[2:]
    if len(switchHex) == 1:
        switchHex = "0"+switchHex
    if len(portHex) == 1:
        portHex = "0"+portHex
    return EthAddr("00:00:00:00:"+switchHex+":"+portHex)


netGraph = nx.Graph()
#adjacency = defaultdict(lambda:defaultdict(lambda:None))
adjacency = np.zeros((101,101))
class Tutorial (object):
  """
  A Tutorial object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection, sid):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    #def startup ():
    self.connection = connection
    self.sid = sid
    #self.mac = dpid_to_mac(sid)
    # This binds our PacketIn event listener
    connection.addListeners(self)

    # Use this table to keep track of which ethernet address is on
    # which switch port (keys are MACs, values are ports).
    self.mac_to_port = {}
    #core.call_when_ready(startup, ('openflow','openflow_discovery'))

  def _handle_LinkEvent(self, event):
    def flip (link):
      return Discovery.Link(link[2], link[3],link[0],link[1])
    #l = event.link
    #sw1 = switches[l.dpid1]
    #sw2 = switches[l.dpis2]
    

  def resend_packet (self, packet_in, out_port):
    """
    Instructs the switch to resend a packet that it had sent to us.
    "packet_in" is the ofp_packet_in object the switch had sent to the
    controller due to a table-miss.
    """
    msg = of.ofp_packet_out()
    msg.data = packet_in

    # Add an action to send to the specified port
    action = of.ofp_action_output(port = out_port)
    msg.actions.append(action)

    # Send message to switch
    self.connection.send(msg)


  def act_like_hub (self, packet, packet_in):
    """
    Implement hub-like behavior -- send all packets to all ports besides
    the input port.
    """
    # We want to output to all ports -- we do that using the special
    # OFPP_ALL port as the output port.  (We could have also used
    # OFPP_FLOOD.)
    self.resend_packet(packet_in, of.OFPP_ALL)

    # Note that if we didn't get a valid buffer_id, a slightly better
    # implementation would check that we got the full data before
    # sending it (len(packet_in.data) should be == packet_in.total_len)).


 
  def act_like_switch (self, packet, packet_in):
    """
    Implement switch-like behavior.
    """

    def drop():
      if event.ofp.buffer_id is not None:
        msg = of.ofp_packet_out()
        msg.buffer_id = event.ofp.buffer_id
        event.ofp.buffer_id = None
        msg.in_port = packet_in.in_port
        self.connection.send(msg)
   
    
    # Here's some psuedocode to start you off implementing a learning
    # switch.  You'll need to rewrite it as real Python code.

    # Learn the port for the source MAC
    #self.mac_to_port ... <add or update entry>
    #print "Switch: " + str(self.sid)
    self.mac_to_port[packet.src] = packet_in.in_port
    import pox.lib.packet as pkt

    if packet.type == packet.LLDP_TYPE:
      drop()
      return
    if packet.type == pkt.ethernet.IPV6_TYPE:
      #drop()
      return
    
    if packet.type == pkt.ethernet.IP_TYPE:
      ipv4_packet = packet.find("ipv4")
      src_ip = ipv4_packet.srcip
      dst_ip = ipv4_packet.dstip
      (nothing, sN, iPt, nada) = str(packet.next.srcip).split(".")
      (nothing, dN, dP, nada) = str(packet.next.dstip).split(".")

      srcNode = int(sN)
#      inPort = int(iPt)
      dstNode = int(dN)
      destPort = int(dP)

      #paths = nx.shortest_path(netGraph,self.sid, int(dstNode))
      allPaths = nx.all_shortest_paths(netGraph, self.sid, int(dstNode))
      listPaths = []
      for p in allPaths:
        listPaths.append(p)
      
      paths = listPaths[randint(0,min(len(listPaths)-1,7))]
      print paths
      print len(listPaths)
      msg = of.ofp_flow_mod()
      #msg.match = of.ofp_match()
      msg.match = of.ofp_match.from_packet(packet)
      #msg.match = of.ofp_match.from_packet(packet)
      #msg.match.in_port = packet_in.in_port
      msg.match.idle_timeout = 10000
      #msg.match.type = pkt.ethernet.IP_TYPE
      #msg.data = packet_in
      print "Received on: " + str(packet_in.in_port)
      if dstNode == self.sid:
        print "ADDING last port as: " + str(destPort)
        msg.actions.append(of.ofp_action_output(port = destPort))
        self.resend_packet (packet_in, destPort)

      else:
        print "Send out of port: " + str(adjacency[paths[0]][paths[1]])
        nextPort = adjacency[paths[0]][paths[1]]
        msg.actions.append(of.ofp_action_output(port = nextPort))
        self.resend_packet ( packet_in, nextPort)
      #print "port: >???"
      #print adjacency
      self.connection.send(msg)
#      for possPath in paths[0]:
 #       print "Path: "
    #      print intNode
    #print packet.effective_ethertype
    elif packet.type == packet.ARP_TYPE:
      if packet.payload.opcode == arp.REQUEST:
        mac_reply = ip_to_mac(packet.payload.protodst)
        print mac_reply
        print packet.payload.protodst
        arp_reply = arp()
        arp_reply.hwsrc = mac_reply
        arp_reply.hwdst = packet.src
        arp_reply.opcode = arp.REPLY
        arp_reply.protosrc = packet.payload.protodst
        arp_reply.protodst = packet.payload.protosrc
        ether = ethernet()
        ether.type = ethernet.ARP_TYPE
        ether.dst = packet.src
        ether.src = mac_reply
        ether.payload = arp_reply
        msg = of.ofp_packet_out()
        msg.data = ether.pack()
        msg.actions.append(of.ofp_action_output(port = of.OFPP_IN_PORT))
        msg.in_port = packet_in.in_port
        self.connection.send(msg)
        
    #return
    elif packet.type != packet.LLDP_TYPE:
    #if True:
      #print "GOT HERE SOMEHOW"
      #print dir(packet)
      #print "Ethertype: " + str(packet.effective_ethertype) + " is not " + str(packet.LLDP_TYPE)
      if packet.dst in self.mac_to_port:
        #if the port associated with the destination MAC of the packet is known:
        # Send packet out the associated port
        self.resend_packet(packet_in, self.mac_to_port[packet.dst])

        # Once you have the above working, try pushing a flow entry
        # instead of resending the packet (comment out the above and
        # uncomment and complete the below.)

        log.debug("Installing flow...")
        # Maybe the log statement should have source/destination/port?

        #msg = of.ofp_flow_mod()
        #
        ## Set fields to match received packet
        #msg.match = of.ofp_match.from_packet(packet)
        #
        #< Set other fields of flow_mod (timeouts? buffer_id?) >
        #
        #< Add an output action, and send -- similar to resend_packet() >

      else:
        # Flood the packet out everything but the input port
        # This part looks familiar, right?
        self.resend_packet(packet_in, of.OFPP_ALL)
        


  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.

    # Comment out the following line and uncomment the one after
    # when starting the exercise.
#    print "Src: " + str(packet.src)
 #   print "Dest: " + str(packet.dst)
  #  print "Event port: " + str(event.port)
    #self.act_like_hub(packet, packet_in)
    #log.info("packet in")
    self.act_like_switch(packet, packet_in)

def CheckController ():

  #  def start_switch (event):
  #   log.debug("Controlling %s" % (event.connection,))
  #  Tutorial(event.connection)

  
  # _neededComponents = set (['openflow_discovery'])
  # if not core.listen_to_dependencies(_neededComponents):
  #   listenTo(core)
  # listenTo(core.openflow)

  
  def __init__ (self):
    def startup():
      core.openflow.addListeners(self, priority=0)
      #core.openflow.addListenerByName("ConnectionUp", start_switch)
    core.call_when_ready(startup, ('openflow'))
      
  def _handle_ConnectionUp(self, event):
    log.debug("Controlling %s" % (event.connection,))
    Tutorial(event.connection)


  
  #core.openflow_disppcovery.addListenerByName("LinkEvent",getTopo)
  #core.openflow_discovery.addListenerByName("LinkEvent",getTopo)
  #core.openflow_discovery.addListeners(self)
  

def launch ():
  """
  Starts the component
  """

  links = {}
  switches = {}
  
  def start_switch (event):
    #def _handle_ConnectionUp(self,event):
    log.debug("Controlling %s" % (event.connection,))
    switches[event.dpid] = Tutorial(event.connection, event.dpid)

  def _handle_BarrierIn(self, event):
    return
    
  # def _handle_LinkEvent (self, event):
  #   l = event.link
  #   netGraph.add_edge(l.dpid1,l.dpid2)
  #   print netGraph.nodes()
  def getTopo (event):
    l = event.link
    #print l.dpid1
    sw1 = switches[l.dpid1]
    sw2 = switches[l.dpid2]

    netGraph.add_edge(l.dpid1,l.dpid2)
    #adjacency[sw1][sw2] = l.port1
    #adjacency[sw2][sw1] = l.port2
    adjacency[l.dpid1][l.dpid2] = l.port1
    adjacency[l.dpid2][l.dpid1] = l.port2
    
    
    #print netGraph.nodes()

  #core.openflow.addListeners()
  def startup():
    core.openflow.addListenerByName("ConnectionUp", start_switch)
    core.openflow_discovery.addListenerByName("LinkEvent",getTopo)

  #core.call_when_ready(startup, ('openflow'))

  core.call_when_ready(startup, ('openflow','openflow_discovery'))
  #core.openflow_discovery.addListeners(self)
  
