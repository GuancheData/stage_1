import mysql.connector
from indexer.src.main.python.metadata.storage.metadata_datamart_container import MetadataDatamartContainer

class MetadataMySQLDB(MetadataDatamartContainer):
    def __init__(self, metadata_parser, dbConfig):
        super().__init__(metadata_parser)
        self.db_config = dbConfig
        self._ensure_database_exists()

    def _ensure_database_exists(self):
        config = self.db_config.copy()
        db_name = config.pop('database')
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.close()
        self.db_config['database'] = db_name

    def save_metadata(self, book_id_set):
        metadata_set = self.metadata_parser.parse_metadata(book_id_set)
        for id, metadata in metadata_set.items():
            self.insert_metadata(
                id=int(id),
                title=metadata.get("Title"),
                author=metadata.get("Author"),
                language=metadata.get("Language")
            )
        if metadata_set:
            print(f"Metadata saved in {self.db_config['database']}.db (MySQL)\n")
            return self.extract_language(metadata_set)

    def insert_metadata(self, id, title, author, language):
        if id is None:
            return "error"
        with mysql.connector.connect(**self.db_config) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    id INT PRIMARY KEY,
                    title TEXT NOT NULL,
                    author VARCHAR(255),
                    language VARCHAR(255)
                );
            """)
            cursor.execute("""
                INSERT INTO metadata (id, title, author, language)
                VALUES (%s, %s, %s, %s)
            """, (id, title, author, language))
            connection.commit()
