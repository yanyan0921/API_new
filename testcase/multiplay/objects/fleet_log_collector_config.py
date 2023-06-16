import uuid

from testcase.multiplay.default import Default


class FleetLogCollectorConfig:
    id = None
    bucket = Default.random_letters()
    secretId = str(uuid.uuid4())
    secretKey = str(uuid.uuid4())
    logPath = Default.random_letters()
    createdBy = Default.random_letters()
    createdAt = None
    modifiedBy = None
    modifiedAt = None

    def __init__(self, *args):
        if len(args) == 1 and type(args[0]) == dict:
            self.id = args[0]['id']
            self.bucket = args[0]['bucket']
            self.secretId = args[0]['secretId']
            self.secretKey = args[0]['secretKey']
            self.logPath = args[0]['logPath']
            self.createdBy = args[0]['createdBy']
            self.createdAt = args[0]['createdAt']
            self.modifiedBy = args[0]['modifiedBy']
            self.modifiedAt = args[0]['modifiedAt']

    def object2dict(self):
        return {
            'id': self.id,
            'bucket': self.bucket,
            'secretId': self.secretId,
            'secretKey': self.secretKey,
            'logPath': self.logPath,
            'createdBy': self.createdBy,
            'createdAt': self.createdAt,
            'modifiedBy': self.modifiedBy,
            'modifiedAt': self.modifiedAt
        }
