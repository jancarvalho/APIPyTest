import os
import random
import typing
import unittest
import pytest
import requests
from typing import Dict, Any, Generator
from source.client_api.book_client import BookClient
from source.client_api.config import ClientAPIConfig

@pytest.fixture(scope="session")
def config_api() -> ClientAPIConfig:
    """
    Fixture to provide Global ClientAPIConfig for tests.
    Returns:
        ClientAPIConfig: The configuration for the Client API.
    """
    return ClientAPIConfig.from_env()

@pytest.fixture(scope="session")
def http_session() -> typing.Generator[requests.Session, None, None]:
    """
    Fixture to provide a requests.Session for HTTP calls.
    Yields:
        requests.Session: The HTTP session.
    """
    session = requests.Session()
    yield session
    session.close()
    
@pytest.fixture(scope="session")
def book_client(config_api: ClientAPIConfig, http_session: requests.Session) -> BookClient:
    """
    Fixture to provide a BookClient instance for tests.
    Args:
        config_api (ClientAPIConfig): The configuration for the Client API.
        http_session (requests.Session): The HTTP session.
    Returns:
        BookClient: The BookClient instance.
    """
    return BookClient(url_base=config_api.url_base, session=http_session)

@pytest.fixture(scope="function")
def random_book_id(book_client: BookClient) -> int:
    """
    Fixture to provide a random valid book ID for tests.
    Args:
        book_client (BookClient): The BookClient instance.
    Returns:
        int: A random valid book ID.
    """
    books = book_client.get_books()
    if not books:
        raise ValueError("No books available to select a random ID from.")
    return random.choice(books)['id']

@pytest.fixture
def valid_book_id(book_client: BookClient, random_book_id: int) -> Dict[str, Any]:
    """
    Fixture to provide a valid book ID for tests.
    Args:
        book_client (BookClient): The BookClient instance.
    Returns:
        int: A valid book ID.
    """
    # books = book_client.get_books()
    book = book_client.build_valid_book_data(random_book_id)
    if not book:
        raise ValueError("No book available to select a valid ID from.")
    return {
        "id": book['id'],
        "title": book['title'],
        "description": book['description'],
        "pageCount": book['pageCount'],
        "excerpt": book['excerpt'],
        "publishDate": book['publishDate']
    }

@pytest.fixture
def sample_book_data() -> dict:
    """
    Fixture to provide sample book data for tests.
    Returns:
        dict: Sample book data.
    """
    return {
        "id": 9999,
        "title": "Sample Book",
        "description": "This is a sample book description.",
        "pageCount": 123,
        "excerpt": "This is a sample excerpt from the book.",
        "publishDate": "2024-01-01T00:00:00Z"
    }
