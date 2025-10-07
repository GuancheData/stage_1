# Search Engine - Stage 1

A comprehensive search engine implementation for processing and indexing book collections with flexible storage backends.

## Repository Structure

```
├── datalake/        # Directory for storing raw book files (input corpus)
├── crawler/         # Source code for web scraping and automated data acquisition (e.g., Project Gutenberg)
├── indexer/         # Core indexing system: metadata extraction, inverted index creation, and storage backend logic
├── query-engine/    # Search functionality, query processing, and retrieval logic for indexed content
├── .gitignore       # Specifies intentionally untracked files to ignore by Git (e.g., .idea, virtual environments)
├── LICENSE          # Project license file (usage and distribution terms)
└── README.md        # Project overview and usage instructions (this file)
```
---

## Features

- **Flexible Architecture:** Modular design with pluggable components
- **Multiple Storage Backends:** 
  - Metadata: CSV, JSON, SQLite, MySQL
  - Inverted Index: MongoDB, Hierarchical folders, Monolithic JSON
- **Scalable Design:** Efficient handling of large book collections
- **Web Crawler:** Automated book collection from Project Gutenberg
- **Query Engine:** Fast full-text search capabilities

---

## Prerequisites

- **Python:** 3.8 or higher
- **MySQL Server:** 5.7 or higher (if using MySQL backend)
- **MongoDB:** 4.4 or higher (if using MongoDB backend)
- **MongoDB Compass:** Optional, for database visualization


---
### 3. Install Python Dependencies

```sh
pip install pymongo mysql-connector-python pandas pytest requests nltk timeit
```

#### Main dependencies:

- **pymongo** – MongoDB backend support
- **mysql-connector-python** – MySQL backend support
- **pandas** – Data manipulation and CSV support
- **pytest** – Testing framework
- **requests** – HTTP requests (for crawler)
- **nltk** – Natural Language Toolkit (for tokenization, etc.)
- **timeit** – Benchmarking and timing code execution

<sub>Note:  
If you use the `nltk` library, you must download its data packages the first time you run your code. You can do this in a Python shell:
```python
import nltk
nltk.download('all')
```
</sub>

---
## Usage
The following usage examples are done by terminal. Alternatively, it is possible to run the modules by creating 
run configurations for both Main.py, using the same parameters
### Crawler

The crawler downloads books from Project Gutenberg and stores them in the datalake.

```sh
python crawler/src/main/python/main.py [datalake_path] [logs_output_path]
```
- All the files of the datalake will be saved in [datalake_path]. If unsure, use "datalake"
- The logs of the downloaded files will be saved in [logs_output_path]. If unsure, use "control"
 
#### Configuration Examples
**Crawler execution: Datalake ordered by ID**

Crawler main.py code:
```python
if __name__ == "__main__":
    datalake_path = sys.argv[1]
    logs_output_path = sys.argv[2]
    crawler = CrawlerController(datalake_path, logs_output_path, datalake_structure="id")
    crawler.download(15)
```
```sh
python crawler/src/main/python/main.py datalake control
```

### Indexer

The indexer processes books and creates searchable indexes using your chosen backends.

#### Basic Usage
##### For monolitic and hierarchical structure:
```sh
python indexer/src/main/python/main.py [datalake_path] [logs_output_path] [inverted_index_output]
```
- All the files of the datalake will be saved in [datalake_path]. If unsure, use "datalake"
- The logs of the downloaded and indexed files will be saved in [logs_output_path]. If unsure, use "control"
- The datamart of with the inverted index files will be saved in [inverted_index_output_folder]. If unsure, use "inverted_index"

##### For mongodb:
```sh
python indexer/src/main/python/main.py [datalake_path] [logs_output_path] (db_name) (collection_name)
```
- All the files of the datalake will be saved in [datalake_path]. If unsure, use "datalake"
- The logs of the downloaded and indexed files will be saved in [logs_output_path]. If unsure, use "control"
- (db_name) and (collection_name) are optional parameters for the mongodb name and the collection name

#### Configuration Examples
**Indexer execution: CSV Metadata + Hierarchical inverted index structure**

Indexer main.py code:
```python
if __name__ == '__main__':
    datalake_path = sys.argv[1]
    logs_output_path = sys.argv[2]
    inverted_index_output_path = sys.argv[3]

    indexer = IndexerController(
        MetadataCSVContainer(
            MetadataParser(datalake_path),
            inverted_index_output_path),
            HierarchicalFolderStructure(
                datalake_path,
                inverted_index_output_path),
        logs_output_path)

    indexer.index()
```
```sh
python indexer/src/main/python/main.py datalake control inverted_index
```

---

## Component Details

### Metadata Layer Options

| Backend   | Class                   | Required Arguments                                     |
|-----------|------------------------|--------------------------------------------------------|
| CSV       | `MetadataCSVContainer`  | `datalakePath`, `outputCSVPath`                        |
| JSON      | `MetadataJSONContainer` | `datalakePath`, `outputJSONPath`                       |
| SQLite    | `MetadataSQLiteDB`      | `datalakePath`, `dbPath`                               |
| MySQL     | `MetadataMySQLDB`       | `datalakePath`, `host`, `user`, `password`, `database` |

### Inverted Index Options

| Backend        | Class                      | Required Arguments                 |
|----------------|---------------------------|------------------------------------|
| MongoDB        | `MongoDB`                  | `datalakePath`                     |
| Hierarchical   | `HierarchicalFolderStructure` | `datalakePath`, `outputFolderPath`|
| Monolithic     | `MonoliticIndexer`         | `outputJSONPath`, `datalakePath`   |



---

## Tests

The tests are located in the `indexer` module and are used to benchmark the various technologies implemented for both the metadata layer and the inverted index.

For metadata-related tests, if you intend to use MySQL, you need to fill in the required fields in `mysql_credentials.py` (found in the `resources` directory).

---

## License 
This project is licensed under GNU General Public License v3.0. See the [LICENSE](LICENSE) file for further details.