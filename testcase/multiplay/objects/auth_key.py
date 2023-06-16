class AuthKey:
    uuid = None
    userId = None
    orgId = None
    accessKey = None
    secretKey = None
    note = None
    expireAt = None
    resourceAge = None

    def __init__(self, *args):
        self.uuid = args[0]['uuid']
        self.userId = args[0]['userId']
        self.orgId = args[0]['orgId']
        self.accessKey = args[0]['accessKey']
        self.secretKey = args[0]['secretKey']
        self.note = args[0]['note']
        self.expireAt = args[0]['expireAt']
        self.resourceAge = args[0]['resourceAge']

    def object2dict(self):
        return {
            'uuid': self.uuid,
            'userId': self.userId,
            'orgId': self.orgId,
            'accessKey': self.accessKey,
            'secretKey': self.secretKey,
            'note': self.note,
            'expireAt': self.expireAt,
            'resourceAge': self.resourceAge
        }
