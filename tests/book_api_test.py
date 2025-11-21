from http import HTTPStatus
from typing import Any, Dict
import pytest
from source.client_api.book_client import BookClient
from source.client_api.config import ClientAPIConfig

def pytest_configure():
    """
    Configure pytest with custom settings if needed.
    """
    pass

def test_get_all_valid_books(book_client: BookClient) -> None:
    """
    Helper function to fetch all valid books from the API.
    Args:
        book_client (BookClient): The BookClient instance.
    Returns:
        List[Dict[str, Any]]: A list of valid books.
    """
    response = book_client.list_books()
    assert response is not None
    assert isinstance(response, list)
    data = response.json()
    # return [book for book in data if 'id' in book and 'title' in book]
    return data

def test_get_valid_book_by_id(book_client: BookClient) -> None:
    """
    Helper function to fetch a valid book ID from the API.
    Args:
        book_client (BookClient): The BookClient instance.
    Returns:
        int: A valid book ID.
    """
    books = book_client.get_existing_book_ids()
    pytest.skip("Skipping test as no valid books are available.") if not books else None
    
    book_id = books[0]
    response = book_client.get_book(book_id)
    assert response is not None
    assert isinstance(response, dict)
    assert response.status_code == HTTPStatus.OK
    book = response.json()
    assert book['id'] == book_id
    
    assert isinstance(book['title'], str)
    
def test_get_nonexistent_book_id(book_client: BookClient) -> None:
    """
    Helper function to fetch a non-existent book ID.
    Args:
        book_client (BookClient): The BookClient instance.
    Returns:
        int: A non-existent book ID.
    """
    existing_ids = book_client.get_existing_book_ids()
    nonexistent_id = max(existing_ids) + 1000 if existing_ids else 1
    response = book_client.get_book(nonexistent_id)
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_create_valid_book(book_client: BookClient, valid_payload: Dict[str, Any]) -> None:
    """
    Helper function to create a valid book in the API.
    Args:
        book_client (BookClient): The BookClient instance.
        valid_payload (Dict[str, Any]): The valid book data to create.
    Returns:
        Dict[str, Any]: The created book data.
    """
    book_data = valid_payload
    response = book_client.create_book(book_data)
    assert response is not None
    assert isinstance(response, dict)
    assert response.status_code == HTTPStatus.CREATED
    created_book = response.json()
    
    for key, value in book_data.items():
        assert created_book[key] == value
        
def test_create_invalid_book(book_client: BookClient, invalid_payload: Dict[str, Any]) -> None:
    """
    Helper function to attempt creating an invalid book in the API.
    Args:
        book_client (BookClient): The BookClient instance.
        invalid_payload (Dict[str, Any]): The invalid book data to create.
    Returns:
        None
    """
    book_data = invalid_payload
    response = book_client.create_book(book_data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    
def test_update_existing_book(book_client: BookClient, book_id: int, update_payload: Dict[str, Any]) -> None:
    """
    Helper function to update an existing book in the API.
    Args:
        book_client (BookClient): The BookClient instance.
        book_id (int): The ID of the book to update.
        update_payload (Dict[str, Any]): The updated book data.
    Returns:
        Dict[str, Any]: The updated book data.
    """
    book_data = update_payload
    response = book_client.update_book(book_id, book_data)
    assert response is not None
    assert isinstance(response, dict)
    assert response.status_code == HTTPStatus.OK
    updated_book = response.json()
    
    for key, value in book_data.items():
        assert updated_book[key] == value
        
def test_update_nonexistent_book(book_client: BookClient, nonexistent_book_id: int, update_payload: Dict[str, Any]) -> None:
    """
    Helper function to attempt updating a non-existent book in the API.
    Args:
        book_client (BookClient): The BookClient instance.
        nonexistent_book_id (int): The ID of the non-existent book to update.
        update_payload (Dict[str, Any]): The updated book data.
    Returns:
        None
    """
    book_data = update_payload
    response = book_client.update_book(nonexistent_book_id, book_data)
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.NOT_FOUND, HTTPStatus.BAD_REQUEST, HTTPStatus.NOT_FOUND)

def test_delete_existing_book(book_client: BookClient, book_id: int) -> None:
    """
    Helper function to delete an existing book from the API.
    Args:
        book_client (BookClient): The BookClient instance.
        book_id (int): The ID of the book to delete.
    Returns:
        None
    """
    response = book_client.delete_book(book_id)
    assert response is not None
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
    
def test_delete_nonexistent_book(book_client: BookClient, nonexistent_book_id: int) -> None:
    """
    Helper function to attempt deleting a non-existent book from the API.
    Args:
        book_client (BookClient): The BookClient instance.
        nonexistent_book_id (int): The ID of the non-existent book to delete.
    Returns:
        None
    """
    response = book_client.delete_book(nonexistent_book_id)
    assert response.status_code in(HTTPStatus.OK, HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND)
    