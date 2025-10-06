from crawler.src.main.python.storage.book_storage import BookStorage

BOOK_START = "*** START OF THE PROJECT GUTENBERG EBOOK"
BOOK_END = "*** END OF THE PROJECT GUTENBERG EBOOK"
class BookStorageId(BookStorage):
    def __init__(self, datalake_path):
        super().__init__(datalake_path)

    def save(self, book_id, content):
        book_id = int(book_id)
        content_separated = super().separate_header(content)

        if not content_separated:
            return False

        header_content, body_content = content_separated
        path = self.get_book_path(book_id)
        header_path = path / f"{book_id}_header.txt"
        body_path = path / f"{book_id}_body.txt"
        with open(header_path, "w", encoding="utf-8") as file:
            file.write(header_content.strip())
        with open (body_path, "w", encoding="utf-8") as file:
            file.write(body_content.strip())
        return str(header_path), str(body_path)

    def get_book_path(self, book_id):
        book_id_str = f"{book_id:04d}"
        if len(book_id_str) % 2 != 0:
            book_id_str = f"0{book_id_str}"
        parts = [book_id_str[i:i + 2] for i in range(0, len(book_id_str), 2)]
        path = self.datalake_path
        for part in parts:
            path = path / part
        path.mkdir(parents=True, exist_ok=True)
        return path
