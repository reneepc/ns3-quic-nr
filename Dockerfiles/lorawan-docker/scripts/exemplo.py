import ns.core
import ns.network
import ns.point_to_point
import ns.applications

import ns.lora
import sys

# Set up logging
ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)

"""
#
nodes = ns.network.NodeContainer()
nodes.Create(2)


dev = ns.lora.LoraNetDevice()
nodes = ns.lora.NodeContainer()
nodes.Create(2)

pointToPoint = ns.point_to_point.PointToPointHelper()
pointToPoint.SetDeviceAttribute("DataRate", ns.core.StringValue("5Mbps"))
pointToPoint.SetChannelAttribute("Delay", ns.core.StringValue("2ms"))

devices = pointToPoint.Install(nodes)

stack = ns.internet.InternetStackHelper()
stack.Install(nodes)

address = ns.internet.Ipv4AddressHelper()
address.SetBase(ns.network.Ipv4Address("10.1.1.0"),
                ns.network.Ipv4Mask("255.255.255.0"))

interfaces = address.Assign(devices)

echoServer = ns.applications.UdpEchoServerHelper(9)

serverApps = echoServer.Install(nodes.Get(1))
serverApps.Start(ns.core.Seconds(1.0))
serverApps.Stop(ns.core.Seconds(10.0))

echoClient = ns.applications.UdpEchoClientHelper(interfaces.GetAddress(1), 9)
echoClient.SetAttribute("MaxPackets", ns.core.UintegerValue(1))
echoClient.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds(1.0)))
echoClient.SetAttribute("PacketSize", ns.core.UintegerValue(1024))

clientApps = echoClient.Install(nodes.Get(0))
clientApps.Start(ns.core.Seconds(2.0))
clientApps.Stop(ns.core.Seconds(10.0))

ns.core.Simulator.Run()
ns.core.Simulator.Destroy()
"""

def CreateNode(pos, channel):
    """
    This function ...
    pos: 	List of floats
    channel: 	LoraNetDevice
    """
    
    dataRateBps = 300
    phyRateSps = 120
    cfHz = 10000
    bwHz = 125
    constSize = 2
    name = "loraTxMode0"
    mod_type = ns.lora.LoraTxMode.LORA 
    
    loraFact = ns.lora.LoraTxModeFactory
    
    loraTxMode = loraFact.CreateMode(
    mod_type, dataRateBps, phyRateSps, cfHz, bwHz, constSize, name)
    
    m0 = ns.lora.LoraModesList()
    m0.AppendMode(loraTxMode)
        
    
    phyFac = ns.core.ObjectFactory()
    phyFac.SetTypeId("ns3::LoraPhyDual")
    
    phyFac.Set("SupportedModesPhy1", ns.lora.LoraModesListValue(m0));
    
    nodes = ns.network.Node(2)
    
    dev = ns.lora.LoraNetDevice()
    dev.SetNode(nodes)
    
    phy = phyFac.Create()
    mac = ns.lora.MacLoraAca()
    mobility = ns.mobility.ConstantPositionMobilityModel()
    trans = ns.lora.LoraTransducerHd()
    
    mobility.SetPosition(pos)
    nodes.AggregateObject(mobility)
    addr = ns.lora.LoraAddress.Allocate()
    mac.SetAddress(addr)
    
    dev.SetPhy(phy)
    dev.SetMac(mac)
    dev.SetChannel(channel)
    dev.SetTransducer(trans)
    nodes.AddDevice(dev)

    return dev
    
m_bytesRx = 0

#def RxPacket(dev, pkt, mode, sender):
#    """
#    This function updates the number of bites received 'm_bytesRx'.
#    
#    NetDevice: 		Net device
#    const Packet: 	Packet
#    int:		Mode
#    const Address &	Sender	
#    """
#  m_bytesRx += pkt.GetSize()
#  return true
  
prop = ns.lora.LoraPropModelIdeal();

channel = ns.lora.LoraChannel()
channel.SetPropagationModel(prop)
pos = ns.core.Vector3D(100,100,50)

gw0 = CreateNode(pos, channel)

addr = gw0.GetAddress()

# Set positions to nodes
x = 50; y = 50; z = 50; n = 2; 
PtrDevice = []

for i in range(0,n):
    node = CreateNode (ns.core.Vector3D(x,y,z), channel)
    PtrDevice.append(node)
    x += 50; y += 50; z += 50;
    hasReachedLimits = ((x == 10000) | (y == 10000) | (z == 10000))
    if hasReachedLimits:
        x = 50; y = 50; z = 50;
       	PtrDevice[i].SetGWAddress(addr);
       	
for i in range(0,n):
    print(PtrDevice[i].GetAddress())
    
# Set gateway to receive packets from end devices node.
#gw0->SetReceiveCallback(MakeCallback(RxPacket, this));
#gw0.SetReceiveCallback()



