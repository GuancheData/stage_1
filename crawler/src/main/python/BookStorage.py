import os

class BookStorage:
    def __init__(self, outputDir = "books"):
        self.outputDir = outputDir
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

    def save(self, bookId, content):
        filename = os.path.join(self.outputDir, f"book_{bookId}.txt")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        return filename