import os

class BookCounter:

    def __init__(self, filePath):
        self.filePath = filePath
        if not os.path.exists(filePath):
            f = open(self.filePath, "x")
            with open(self.filePath, "w") as file:
                file.write("0")

    def getId(self):
        with open(self.filePath, "r") as file:
            return file.read()

    def increaseBookId(self):
        var = int(self.getId())
        with open(self.filePath, "w") as file:
            file.truncate()
            file.write(str(var + 1))