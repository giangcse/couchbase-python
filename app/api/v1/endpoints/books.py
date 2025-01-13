from typing import List

from fastapi import APIRouter, Depends, HTTPException
from couchbase.exceptions import DocumentNotFoundException

from app.schemas.book import Book, BookCreate, BookUpdate
from app.services.book_service import (
    get_books,
    get_book,
    create_book,
    update_book,
    delete_book,
)
from app.utils.utils import get_current_user

router = APIRouter()

@router.get("/", response_model=List[Book])
async def read_books(current_user: dict = Depends(get_current_user)):
    books = await get_books()
    return books

@router.get("/{book_id}", response_model=Book)
async def read_book(book_id: str, current_user: dict = Depends(get_current_user)):
    try:
        book = await get_book(book_id)
        return book
    except DocumentNotFoundException:
        raise HTTPException(status_code=404, detail="Book not found")

@router.post("/", response_model=Book)
async def create_new_book(book: BookCreate, current_user: dict = Depends(get_current_user)):
    return await create_book(book)

@router.put("/{book_id}", response_model=Book)
async def update_existing_book(
    book_id: str, book: BookUpdate, current_user: dict = Depends(get_current_user)
):
    try:
        updated_book = await update_book(book_id, book)
        return updated_book
    except DocumentNotFoundException:
        raise HTTPException(status_code=404, detail="Book not found")

@router.delete("/{book_id}")
async def delete_existing_book(
    book_id: str, current_user: dict = Depends(get_current_user)
):
    try:
        await delete_book(book_id)
        return {"message": "Book deleted successfully"}
    except DocumentNotFoundException:
        raise HTTPException(status_code=404, detail="Book not found")