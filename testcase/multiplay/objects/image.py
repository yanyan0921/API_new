from testcase.multiplay.default import Default


class Image:
    id = None
    name = Default.random_letters()
    nameInProvider = Default.random_letters()
    os = Default.random_letters()
    size = '100'
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
            self.os = args[0]['os']
            self.size = args[0]['size']
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
            'os': self.os,
            'size': self.size,
            'createdBy': self.createdBy,
            'createdAt': self.createdAt,
            'modifiedBy': self.modifiedBy,
            'modifiedAt': self.modifiedAt,
            'isDeleted': self.isDeleted
        }
