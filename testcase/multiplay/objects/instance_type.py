from testcase.multiplay.default import Default


class InstanceType:
    id = None
    name = Default.random_letters()
    nameInProvider = Default.random_letters()
    cpuType = Default.random_letters()
    cores = 4
    cpuFrequency = 3500
    ram = '8000'
    networkBandwidth = 1000
    gpuType = Default.random_letters()
    createdBy = Default.random_letters()
    createdAt = None
    modifiedBy = None
    modifiedAt = None
    isDeleted = True

    def __init__(self, *args):
        if len(args) == 1 and type(args[0]) == dict:
            self.id = args[0]['id']
            self.name = args[0]['name']
            self.nameInProvider = args[0]['nameInProvider']
            self.cpuType = args[0]['cpuType']
            self.cores = args[0]['cores']
            self.cpuFrequency = args[0]['cpuFrequency']
            self.ram = args[0]['ram']
            self.networkBandwidth = args[0]['networkBandwidth']
            self.gpuType = args[0]['gpuType']
            self.createdBy = args[0]['createdBy']
            self.createdAt = args[0]['createdAt']
            self.modifiedBy = args[0]['modifiedBy']
            self.modifiedAt = args[0]['modifiedAt']
            self.isDeleted = args[0]['isDeleted']

    def object2dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'nameInProvider': self.nameInProvider,
            'cpuType': self.cpuType,
            'cores': self.cores,
            'cpuFrequency': self.cpuFrequency,
            'ram': self.ram,
            'networkBandwidth': self.networkBandwidth,
            'gpuType': self.gpuType,
            'createdBy': self.createdBy,
            'createdAt': self.createdAt,
            'modifiedBy': self.modifiedBy,
            'modifiedAt': self.modifiedAt,
            'isDeleted': self.isDeleted
        }
