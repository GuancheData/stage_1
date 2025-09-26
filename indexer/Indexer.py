import os
import re
import json

class Indexer:
    def __init__(self, booksDir):
        self.booksDir = booksDir
        self.invertedIndex = {}

    def buildIndex(self):
        for filename in os.listdir(self.booksDir):
            if filename.endswith('.txt'):
                filePath = os.path.join(self.booksDir, filename)
                with open(filePath, 'r', encoding='utf-8') as f:
                    text = f.read()
                    words = re.findall(r'\w+', text.lower())
                    for word in words:
                        if word not in self.invertedIndex:
                            self.invertedIndex[word] = set()
                        self.invertedIndex[word].add(filename)

    def saveIndex(self, filename):
        indexToSave = {word: list(files) for word, files in self.invertedIndex.items()}
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(indexToSave, f)