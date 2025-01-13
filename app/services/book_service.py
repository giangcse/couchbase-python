import uuid
from typing import List
from app.db.session import cluster, collection  # Import cluster and collection
from couchbase.result import QueryResult
from couchbase.exceptions import DocumentNotFoundException
from app.schemas.book import Book, BookCreate, BookUpdate
from app.core.config import settings
from couchbase.options import QueryOptions

async def get_books() -> List[Book]:
    query = "SELECT META(b).id, b.* FROM `{}` b WHERE b.type = 'book'".format(
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
    book_id = f"book::{uuid.uuid4()}"
    book_data = {**book.model_dump(), "type": "book"}
    collection.insert(book_id, book_data)
    return Book(id=book_id, **book_data)

async def update_book(book_id: str, book: BookUpdate) -> Book:
    try:
        result = collection.get(book_id)
        existing_book = result.content_as[dict]
        for key, value in book.model_dump(exclude_unset=True).items():
            existing_book[key] = value
        collection.replace(book_id, existing_book)
        return Book(id=book_id, **existing_book)
    except DocumentNotFoundException:
        raise

async def delete_book(book_id: str):
    try:
        collection.remove(book_id)
    except DocumentNotFoundException:
        raise