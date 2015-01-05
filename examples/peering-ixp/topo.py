"""
Example topology of Bird routers
"""

import inspect
import os
from mininext.topo import Topo
from mininext.services.bird import BirdService
from mininet.net import Mininet
from collections import namedtuple

BirdHost = namedtuple("BirdHost", "name ip loIP")
net = None


class BirdTopo(Topo):

    "Creates a topology of Bird routers"

    def __init__(self):
        """Initialize a Bird topology with 5 routers, configure their IP
           addresses, loop back interfaces, and paths to their private
           configuration directories."""
        Topo.__init__(self)

        # Directory where this file / script is located"
        selfPath = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))  # script directory

        # Initialize a service helper for Bird with default options
        BirdSvc = BirdService(autoStop=False)

        # Path configurations for mounts
        BirdBaseConfigPath = selfPath + '/configs/'

        # List of Bird host configs
        BirdHosts = []
	BirdClient = []
	BirdRS = []
        BirdHosts.append(BirdHost(name='Peer1', ip='172.0.1.1/16',
                                      loIP='10.0.1.1/24'))
        BirdHosts.append(BirdHost(name='Peer2', ip='172.0.2.1/16',
                                      loIP='10.0.2.1/24'))
        BirdClient.append(BirdHost(name='Client1', ip='192.168.1.2/24',
                                      loIP='10.0.3.1/24'))
        BirdClient.append(BirdHost(name='Client2', ip='192.168.1.3/24',
                                      loIP='10.0.4.1/24'))
        BirdRS.append(BirdHost(name='rs', ip='172.0.254.254/16',loIP=None))

        # Add switch for IXP fabric
        ixpfabric = self.addSwitch('fabric-sw1')
	clientsw = self.addSwitch('fabric-sw2')
        # Setup each Bird router, add a link between it and the IXP fabric
        for host in BirdHosts:

            # Create an instance of a host, called a BirdContainer
            BirdContainer = self.addHost(name=host.name,
                                           ip=host.ip,
					   
                                           hostname=host.name,
                                           privateLogDir=True,
                                           privateRunDir=True,
                                           inMountNamespace=True,
                                           inPIDNamespace=True,
                                           inUTSNamespace=True)

            # Add a loopback interface with an IP in router's announced range
            self.addNodeLoopbackIntf(node=host.name, ip=host.loIP)

            # Configure and setup the Bird service for this node
            BirdSvcConfig = \
                {'BirdConfigPath': BirdBaseConfigPath + host.name}
            self.addNodeService(node=host.name, service=BirdSvc,
                                nodeConfig=BirdSvcConfig)

            # Attach the BirdContainer to the IXP Fabric Switch
            self.addLink(BirdContainer, ixpfabric)

	for host in BirdClient:

            # Create an instance of a host, called a BirdContainer
            BirdClientContainer = self.addHost(name=host.name,
                                           ip=host.ip,
					 
                                           hostname=host.name,
                                           privateLogDir=True,
                                           privateRunDir=True,
                                           inMountNamespace=True,
                                           inPIDNamespace=True,
                                           inUTSNamespace=True)

            # Add a loopback interface with an IP in router's announced range
            # Add a loopback interface with an IP in router's announced range
            self.addNodeLoopbackIntf(node=host.name, ip=host.loIP)

            # Configure and setup the Bird service for this node
            BirdSvcConfig = \
                {'BirdConfigPath': BirdBaseConfigPath + host.name}
            self.addNodeService(node=host.name, service=BirdSvc,
                                nodeConfig=BirdSvcConfig)

            # Attach the BirdContainer to the IXP Fabric Switch
            self.addLink(BirdClientContainer, clientsw)


	BirdRSContainer = self.addHost(name='rs',
                                           ip='172.0.254.254/16',
					   
                                           hostname='rs',
                                           privateLogDir=True,
                                           privateRunDir=True,
                                           inMountNamespace=True,
                                           inPIDNamespace=True,
                                           inUTSNamespace=True)

	
	
	
	# Configure and setup the Bird service for this node
        BirdSvcConfig = \
        {'BirdConfigPath': BirdBaseConfigPath + 'rs'}
        
	self.addNodeService(node='rs', service=BirdSvc,
                                nodeConfig=BirdSvcConfig)
            	

	self.addLink(BirdRSContainer, ixpfabric)
	self.addLink(BirdRSContainer, clientsw)
