import os

class HierarchicalFolderStructure:
    def __init__(self, databaseName=".../control/HierarchicalFolderStructure/datamart/"):
        self.databaseName = databaseName
        os.makedirs(self.databaseName, exist_ok=True)
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            os.makedirs(os.path.join(self.databaseName, letter), exist_ok=True)



    def insertInformation(self, bookId, wordFrecuence):
        files_data = {}
        for word, freq in wordFrecuence.items():
            firstWord = word[0].upper()
            file_path = os.path.join(self.databaseName, firstWord, f"{word}.txt")
            files_data.setdefault(file_path, []).append(f"{bookId},{freq}\n")
        for file_path, lines in files_data.items():
            with open(file_path, 'a', encoding='utf-8') as f:
                f.writelines(lines)

