"""
Example service that manages Bird routers
"""

from mininext.mount import MountProperties, ObjectPermissions, PathProperties
from mininext.moduledeps import serviceCheck
from mininext.service import Service


class BirdService(Service):

    "Manages Bird Software Router Service"

    def __init__(self, name="Bird", **params):
        """Initializes a BirdService instance with a set of global parameters

        Args:
            name (str): Service name (derived class may wish to override)
            params: Arbitrary length list of global properties for this service

        """

        # Verify that Bird is installed"
        #serviceCheck('Bird', moduleName='Bird (nongnu.org/Bird/)')

        # Call service initialization (will set defaultGlobalParams)
        Service.__init__(self, name=name, **params)

        self.getDefaultGlobalMounts()

    def verifyNodeMeetsServiceRequirements(self, node):
        """Verifies that a specified node is configured to support Bird

        Overrides the :class:`.Service` default verification method to conduct
            checks specific to Bird. This includes checking that the node
            has a private log space, a private run space, and is in a PID
            namespace

        Args:
            node: Node to inspect

        """

        if node.inPIDNamespace is False:
            raise Exception("Bird service requires PID namespace (node %s)\n"
                            % (node))

        if node.hasPrivateLogs is False:
            raise Exception("Bird service requires private logs (node %s)\n"
                            % (node))

        if node.hasPrivateRun is False:
            raise Exception("Bird service requires private /run (node %s)\n"
                            % (node))

    def setupNodeForService(self, node):
        """After mounts and other operations taken care of by Service Helper,
           we perform a few last minute tasks here"""

        # Initialize log directory
        #_, err, ret = node.pexec("mkdir /var/log/Bird")
        #_, err, ret = node.pexec("chown Bird:Bird /var/log/Bird")

    def getDefaultGlobalParams(self):
        "Returns the default parameters for this service"
        defaults = {'startCmd': '/etc/init.d/bird start',
                    'stopCmd': '/etc/init.d/bird stop',
                    'autoStart': True,
                    'autoStop': True,
                    'configPath': None}
        return defaults

    def getDefaultGlobalMounts(self):
        "Service-wide default mounts for the Bird service"

        mounts = []
        mountConfigPairs = {}

        # Bird configuration paths
        BirdConfigPerms = ObjectPermissions(username='bird',
                                              groupname='bird',
                                              mode=0o775,
                                              strictMode=False,
                                              enforceRecursive=True)
        BirdConfigPath = PathProperties(path=None,
                                          perms=BirdConfigPerms,
                                          create=True,
                                          createRecursive=True,
                                          setPerms=True,
                                          checkPerms=True)
        BirdConfigMount = MountProperties(target='/etc/bird',
                                            source=BirdConfigPath)
        mounts.append(BirdConfigMount)
        mountConfigPairs['BirdConfigPath'] = BirdConfigMount

        return mounts, mountConfigPairs
