import os


class DirParser:

    def __init__(self, root):
        self.files = []
        self.names = []
        self.root = root

    def list_dir(self, root):
        for filename in os.listdir(root):
            pathname = os.path.join(root, filename)
            if os.path.isfile(pathname):
                self.files.append(pathname.replace('\\', '/'))
                self.names.append(filename)
            elif os.path.isdir(pathname):
                self.list_dir(pathname)

    def search_folder(self, folders):
        for folder in folders:
            self.list_dir(self.root + folder + '/')

    def get_folder_files(self, folders):
        self.search_folder(folders)
        return self.files

    def get_files(self, names):
        testcases = []
        self.list_dir(self.root)
        for name in names:
            name += '.json'
            if name in self.names:
                testcases.append(self.files[self.names.index(name)])
        return testcases


