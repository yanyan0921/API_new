from testcase.multiplay.default import Default


class FleetRegionProvider:
    id = None
    name = Default.random_letters()
    fleetId = None
    regionId = None
    providerType = Default.random_letters()
    providerConfig = Default.random_letters()
    createdBy = Default.random_letters()
    createdAt = None
    modifiedBy = None
    modifiedAt = None
    resourceAge = 0

    def __init__(self, *args):
        if len(args) == 2 and type(args[0]) == str and type(args[1]) == str:
            self.fleetId = args[0]
            self.regionId = args[1]
            self.name = Default.random_letters()
            self.providerType = Default.random_letters()
            self.providerConfig = Default.random_letters()
            self.createdBy = Default.random_letters()
        if len(args) == 1 and type(args[0]) == dict:
            self.id = args[0]['id']
            self.name = args[0]['name']
            self.fleetId = args[0]['fleetId']
            self.regionId = args[0]['regionId']
            self.providerType = args[0]['providerType']
            self.providerConfig = args[0]['providerConfig']
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
            'regionId': self.regionId,
            'providerType': self.providerType,
            'providerConfig': self.providerConfig,
            'createdBy': self.createdBy,
            'createdAt': self.createdAt,
            'modifiedBy': self.modifiedBy,
            'modifiedAt': self.modifiedAt,
            'resourceAge': self.resourceAge
        }
