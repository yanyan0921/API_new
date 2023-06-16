class Allocation:
    uuid = 'string'
    fleetId = 'string'
    regionId = 'string'
    profileId = 'string'
    status = 'string'
    message = 'string'
    instanceId = 'string'
    instanceName = 'string'
    ip = 'string'
    port = 0
    createdBy = 'string'
    createdAt = None
    fulfilledAt = None
    deletedAt = None

    def __init__(self, *args):
        if len(args) == 1 and type(args[0]) == dict:
            self.uuid = args[0]['uuid']
            self.fleetId = args[0]['fleetId']
            self.regionId = args[0]['regionId']
            self.profileId = args[0]['profileId']
            self.status = args[0]['status']
            self.message = args[0]['message']
            self.instanceId = args[0]['instanceId']
            self.instanceName = args[0]['instanceName']
            self.ip = args[0]['ip']
            self.port = args[0]['port']
            self.createdBy = args[0]['createdBy']
            self.createdAt = args[0]['createdAt']
            self.fulfilledAt = args[0]['fulfilledAt']
            self.deletedAt = args[0]['deletedAt']

    def object2dict(self):
        return {
            'uuid': self.uuid,
            'fleetId': self.fleetId,
            'regionId': self.regionId,
            'profileId': self.profileId,
            'status': self.status,
            'message': self.message,
            'instanceId': self.instanceId,
            'instanceName': self.instanceName,
            'ip': self.ip,
            'port': self.port,
            'createdBy': self.createdBy,
            'createdAt': self.createdAt,
            'fulfilledAt': self.fulfilledAt,
            'deletedAt': self.deletedAt
        }
