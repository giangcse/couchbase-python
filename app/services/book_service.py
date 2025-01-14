import uuid
from typing import List
from app.db.session import cluster, get_book_collection
from couchbase.result import QueryResult
from couchbase.exceptions import DocumentNotFoundException
from app.schemas.book import Book, BookCreate, BookUpdate
from app.core.config import settings
from couchbase.options import QueryOptions
from sentence_transformers import SentenceTransformer

collection = get_book_collection()

# Load mô hình embedding
model = SentenceTransformer('all-MiniLM-L6-v2')

async def get_books(search = None) -> List[Book]:
    if not search:
        query = "SELECT META(b).id, b.* FROM `{}`.bookscope.books b WHERE b.type = 'book'".format(
            settings.COUCHBASE_BUCKET
        )
        # Thực hiện truy vấn trên đối tượng cluster, truyền QueryOptions để có kết quả Async
        result: QueryResult = cluster.query(query, QueryOptions(adhoc=False)) 
        
        # Sử dụng result.rows() trực tiếp trong list comprehension, không cần await
        books = [
            Book(
                id=row["id"],
                title=row["title"],
                author=row["author"],
                description=row["description"],
                summary=row["summary"],
                 summary_vector = row.get("summary_vector")
            )
            for row in result.rows()
        ]
        return books
    else:
       
        # Tạo vector embedding cho query
        query_embedding = model.encode(search).tolist()
        query = """
            SELECT META(b).id, b.*
            FROM `{0}`.bookscope.books AS b
            WHERE SEARCH(b, {{"vector": {{"field": "summary_vector", "k": 10, "top_k": 10,"query_vector": {1} }}}}
                )
        """.format(settings.COUCHBASE_BUCKET, query_embedding)
        result: QueryResult = cluster.query(query, QueryOptions(adhoc=False))
        books = [
            Book(
                id=row["id"],
                title=row["title"],
                author=row["author"],
                description=row["description"],
                summary=row["summary"],
                summary_vector = row.get("summary_vector")
             )
            for row in result.rows()
            ]
        return books


async def get_book(book_id: str) -> Book:
    try:
        result = collection.get(book_id)
        book_data = result.content_as[dict]
        return Book(id=book_id, **book_data)
    except DocumentNotFoundException:
        raise

async def create_book(book: BookCreate) -> Book:
     # Tạo vector embedding cho summary
    embedding = model.encode(book.summary or "").tolist() if book.summary else None
    book_id = f"{uuid.uuid4()}"
    book_data = {**book.model_dump(), "type": "book", "summary_vector": embedding}
    collection.insert(book_id, book_data)
    return Book(id=book_id, **book_data)

async def update_book(book_id: str, book: BookUpdate) -> Book:
    try:
         result = collection.get(book_id)
         existing_book = result.content_as[dict]

         # Tạo vector embedding cho summary
         embedding = model.encode(book.summary or "").tolist()  if book.summary else None

         for key, value in book.model_dump(exclude_unset=True).items():
              existing_book[key] = value
              
         existing_book["summary_vector"] = embedding
         
         collection.replace(book_id, existing_book)
         return Book(id=book_id, **existing_book)
    except DocumentNotFoundException:
        raise

async def delete_book(book_id: str):
    try:
        collection.remove(book_id)
    except DocumentNotFoundException:
        raise