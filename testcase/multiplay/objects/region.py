from testcase.multiplay.default import Default


class Region:
    id = None
    name = Default.random_letters()
    nameInProvider = Default.random_letters()
    regionConfig = Default.random_letters()
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
            self.regionConfig = args[0]['regionConfig']
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
            'regionConfig': self.regionConfig,
            'createdBy': self.createdBy,
            'createdAt': self.createdAt,
            'modifiedBy': self.modifiedBy,
            'modifiedAt': self.modifiedAt,
            'isDeleted': self.isDeleted
        }
