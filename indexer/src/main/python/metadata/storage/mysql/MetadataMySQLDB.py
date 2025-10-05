import mysql.connector
from indexer.src.main.python.metadata.storage.MetadataDatamartContainer import MetadataDatamartContainer

class MetadataMySQLDB(MetadataDatamartContainer):
    def __init__(self, dbConfig):
        super().__init__()
        self.dbConfig = dbConfig
        self._ensure_database_exists()

    def _ensure_database_exists(self):
        config = self.dbConfig.copy()
        db_name = config.pop('database')
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.close()
        self.dbConfig['database'] = db_name

    def saveMetadata(self, idSet):
        metadataSet = self.parser.parseMetadata(idSet)
        for id, metadata in metadataSet.items():
            self.insertMetadata(
                id=int(id),
                title=metadata.get("Title"),
                author=metadata.get("Author"),
                language=metadata.get("Language")
            )
        if metadataSet:
            print(f"Metadata saved in {self.dbConfig['database']}.db (MySQL)\n")
            return self.extractLanguage(metadataSet)

    def insertMetadata(self, id, title, author, language):
        if id is None:
            return "error"
        with mysql.connector.connect(**self.dbConfig) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    id INT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    author VARCHAR(255),
                    language VARCHAR(255)
                );
            """)
            cursor.execute("""
                INSERT INTO metadata (id, title, author, language)
                VALUES (%s, %s, %s, %s)
            """, (id, title, author, language))
            connection.commit()