import os
import requests

# TODO: Refactor code and see if there is a more efficient way. Also, start to create a new class or method to
#  save all the txt.
class Crawler:

    def __init__(self, fileDir):
        self.fileDir = fileDir
        if not os.path.exists(fileDir):
            f = open(self.fileDir, "x")
            with open(self.fileDir, "w") as file:
                file.write("0")


    def request(self):
        request = requests.get(self.getUrl(self.getId()))
        if request.status_code == 200:
            print(request.text)
        else:
            print("There is no book")
        self.increaseBookId()


    def getUrl(self, id):
        return f"https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt"

    def getId(self):
        with open(self.fileDir, "r") as file:
            return file.read()

    def increaseBookId(self):
        var = int(self.getId())
        with open(self.fileDir, "w") as file:
            file.truncate()
            file.write(str(var + 1))