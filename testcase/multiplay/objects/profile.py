from testcase.multiplay.default import Default


class Profile:
    id = None
    name = Default.random_letters()
    fleetId = None
    workingDir = Default.random_letters()
    binaryName = Default.random_letters()
    arguments = Default.random_letters()
    binaryLocation = Default.random_letters()
    binaryVersion = None
    keepAlive = True
    port = str(Default.random_int())
    logPath = Default.random_letters()
    createdBy = Default.random_letters()
    createdAt = None
    modifiedBy = None
    modifiedAt = None
    resourceAge = None

    def __init__(self, *args):
        if len(args) == 1 and type(args[0]) == str:
            self.name = Default.random_letters()
            self.fleetId = args[0]
            self.workingDir = Default.random_letters()
            self.binaryName = Default.random_letters()
            self.arguments = Default.random_letters()
            self.binaryLocation = Default.random_letters()
            self.port = str(Default.random_int())
            self.logPath = Default.random_letters()
            self.createdBy = Default.random_letters()
        if len(args) == 1 and type(args[0]) == dict:
            self.id = args[0]['id']
            self.name = args[0]['name']
            self.fleetId = args[0]['fleetId']
            self.workingDir = args[0]['workingDir']
            self.binaryName = args[0]['binaryName']
            self.arguments = args[0]['arguments']
            self.binaryLocation = args[0]['binaryLocation']
            self.binaryVersion = args[0]['binaryVersion']
            self.keepAlive = args[0]['keepAlive']
            self.port = args[0]['port']
            self.logPath = args[0]['logPath']
            self.createdBy = args[0]['createdBy']
            self.createdAt = args[0]['createdAt']
            self.modifiedBy = args[0]['modifiedBy']
            self.modifiedAt = args[0]['modifiedAt']
            self.resourceAge = args[0]['resourceAge']

    def object2dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'fleetId': self.fleetId,
            'workingDir': self.workingDir,
            'binaryName': self.binaryName,
            'arguments': self.arguments,
            'binaryLocation': self.binaryLocation,
            'binaryVersion': self.binaryVersion,
            'keepAlive': self.keepAlive,
            'port': self.port,
            'logPath': self.logPath,
            'createdBy': self.createdBy,
            'createdAt': self.createdAt,
            'modifiedBy': self.modifiedBy,
            'modifiedAt': self.modifiedAt,
            'resourceAge': self.resourceAge
        }
