from testcase.multiplay.default import Default


class FleetRegion:
    id = None
    fleetId = 'string'
    regionId = 'string'
    minAvailableInstances = 0
    maxInstances = 1
    createdBy = Default.random_letters()
    createdAt = None
    modifiedBy = None
    modifiedAt = None
    isDeleted = False

    def __init__(self, *args):
        if len(args) == 2 and type(args[0]) == str and type(args[1]) == str:
            self.fleetId = args[0]
            self.regionId = args[1]
            self.createdBy = Default.random_letters()
        if len(args) == 1 and type(args[0]) == dict:
            self.id = args[0]['id']
            self.fleetId = args[0]['fleetId']
            self.regionId = args[0]['regionId']
            self.minAvailableInstances = args[0]['minAvailableInstances']
            self.maxInstances = args[0]['maxInstances']
            self.createdBy = args[0]['createdBy']
            self.createdAt = args[0]['createdAt']
            self.modifiedBy = args[0]['modifiedBy']
            self.modifiedAt = args[0]['modifiedAt']
            self.isDeleted = args[0]['isDeleted']

    def object2dict(self):
        return {
            'id': self.id,
            'fleetId': self.fleetId,
            'regionId': self.regionId,
            'minAvailableInstances': self.minAvailableInstances,
            'maxInstances': self.maxInstances,
            'createdBy': self.createdBy,
            'createdAt': self.createdAt,
            'modifiedBy': self.modifiedBy,
            'modifiedAt': self.modifiedAt,
            'isDeleted': self.isDeleted
        }
