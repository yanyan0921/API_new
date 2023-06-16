from testcase.multiplay.default import Default


class Fleet:
    id = None
    name = Default.random_letters()
    instanceTypeId = 0
    imageId = 0
    minAvailableInstances = 0
    maxInstances = 1
    createdBy = Default.random_letters()
    createdAt = None
    modifiedBy = None
    modifiedAt = None
    isDeleted = True

    def __init__(self, *args):
        if len(args) == 2 and type(args[0]) == str and type(args[1]) == str:
            self.instanceTypeId = args[0]
            self.imageId = args[1]
            self.name = Default.random_letters()
            self.createdBy = Default.random_letters()
        if len(args) == 1 and type(args[0]) == dict:
            self.id = args[0]['id']
            self.name = args[0]['name']
            self.instanceTypeId = args[0]['instanceTypeId']
            self.imageId = args[0]['imageId']
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
            'name': self.name,
            'instanceTypeId': self.instanceTypeId,
            'imageId': self.imageId,
            'minAvailableInstances': self.minAvailableInstances,
            'maxInstances': self.maxInstances,
            'createdBy': self.createdBy,
            'createdAt': self.createdAt,
            'modifiedBy': self.modifiedBy,
            'modifiedAt': self.modifiedAt,
            'isDeleted': self.isDeleted
        }
