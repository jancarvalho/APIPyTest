from dataclasses import dataclass, asdict, field
import os
from typing import Optional, Dict, Any, List
import requests
from .config import ClientAPIConfig
import urllib3

@dataclass
class BookClientConfig:
    """
    Configuration for the Book API client.
    Attributes:
        url_base (str): The base URL for the Book API.
        url_base: str = "https://fakerestapi.azurewebsites.net"
        schema api: defines all the schemas for the API
    """
    url_base: str = "https://fakerestapi.azurewebsites.net"
    schema_api: Dict[str, Any] = field(default_factory=dict)
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    pageCount: Optional[int] = None
    excerpt: Optional[str] = None
    publishDate: Optional[str] = None # ISO 8601 format "YYYY-MM-DDTHH:MM:SSZ"

@dataclass
class Book:
    """
    Configuration for the Book API client.
    Attributes:
        url_base (str): The base URL for the Book API.
        url_base: str = "https://fakerestapi.azurewebsites.net"
        schema api: defines all the schemas for the API
    """
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    pageCount: Optional[int] = None
    excerpt: Optional[str] = None
    publishDate: Optional[str] = None # ISO 8601 format "YYYY-MM-DDTHH:MM:SSZ"
class BookClient:
    """
    Client for interacting with the Book API.
    Reusable client to interact with the Book API.
    To know how to use it, please refer to the official documentation: https://fakerestapi.azurewebsites.net/index.html

    Attributes:
        config (ClientAPIConfig): Configuration for the client.
    """
    config: ClientAPIConfig
    
    def __init__(
        self, 
        url_base: Optional[str] = None, 
        session: Optional[requests.Session] = None
    ):
        """
        Initialize the BookClient.

        SSL logic:
        - If REQUESTS_CA_BUNDLE or SSL_CERT_FILE exists → use it (proper SSL)
        - Else → disable SSL verification (verify=False) to avoid SSLError on dev machines
        but GitHub Actions / cloud runners will use valid certs and ignore this fallback.
        """

        # Hide warnings only when verify=False
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Load config from environment
        self.config = ClientAPIConfig.from_env(url_base=url_base)

        # Prepare HTTP session
        self.session = session if session is not None else requests.Session()

        # ========== 🔐 SSL FIX / FALLBACK LOGIC ==========

        # 1. Try to use CA bundle if provided
        ca_bundle = os.getenv("REQUESTS_CA_BUNDLE") or os.getenv("SSL_CERT_FILE")

        if ca_bundle:
            # Use the certificate bundle provided by user/environment
            self.session.verify = ca_bundle
        else:
            # 2. No CA available → disable SSL verification (ONLY for local dev)
            self.session.verify = False
        
        def get_all_books(self):
            """Obtém todos os livros da API."""
            response = self.session.get(f"{self.config.url_base}/api/v1/Books")
            response.raise_for_status()
            return response.json()
        
    @property
    def url_base(self) -> str:
        """
        Get the base URL for the Book API.
        Returns:
            str: The base URL.
        """
        return self.config.url_base
    
    def _url(self, path: str) -> str:
        """
        Construct the full URL for a given API path.
        Args:
            path (str): The API path.
        Returns:
            str: The full URL.
        """
        return f"{self.config.url_base}/{path.lstrip('/')}"
    
    def list_books(self) -> requests.Response:
        """
        Fetch a list of books from the API.

        Returns:
            requests.Response: The response object containing the list of books.
        """
        response = requests.get(self._url("/api/v1/Books"))
        response.raise_for_status()
        return response
    
    def get_book(self, book_id: int) -> requests.Response:
        """
        Fetch a single book by its ID.

        Args:
            book_id (int): The ID of the book to fetch.

        Returns:
            Dict[str, Any]: The book data.
        """
        response = requests.get(f"{self.config.url_base}/api/v1/Books/{book_id}")
        # response.raise_for_status()
        return response
    
    def create_book(self, book_data: Dict[str, Any]) -> requests.Response:
        """
        Create a new book in the API.

        Args:
            book_data (Dict[str, Any]): The data for the new book.

        Returns:
            Dict[str, Any]: The created book data.
        """
        payload = book_data if isinstance(book_data, dict) else book_data
        
        response = requests.post(
            f"{self.config.url_base}/api/v1/Books",
            json=payload
        )
        # response.raise_for_status()
        return response
    
    def update_book(self, book_id: int, book_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing book in the API.

        Args:
            book_id (int): The ID of the book to update.
            book_data (BookClientConfig): The updated data for the book.

        Returns:
            Dict[str, Any]: The updated book data.
        """
        payload = book_data if isinstance(book_data, dict) else book_data

        response = requests.put(
            f"{self.config.url_base}/api/v1/Books/{book_id}",
            json=payload
        )
        response.raise_for_status()
        return response
    
    def delete_book(self, book_id: int) -> None:
        """
        Delete a book from the API.

        Args:
            book_id (int): The ID of the book to delete.
        """
        response = requests.delete(self._url(f"/api/v1/Books/{book_id}"))
        response.raise_for_status()
        return response
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Fetch the API schema.

        Returns:
            Dict[str, Any]: The API schema.
        """
        response = requests.get(self._url("/swagger/v1/swagger.json"))
        response.raise_for_status()
        return response
    
    def get_book_schema(self) -> Dict[str, Any]:
        """
        Fetch the schema for the Book model.

        Returns:
            Dict[str, Any]: The Book model schema.
        """
        schema = self.get_schema()
        return schema.get("definitions", {}).get("Book", {})
    
    def get_existing_book_ids(self) -> List[int]:
        """
        Fetch a list of existing book IDs from the API.

        Returns:
            List[int]: A list of existing book IDs.
        """
        response = self.list_books()
        response.raise_for_status()
        books = response.json()
        
        return [book["id"] for book in books] if isinstance(books, list) else []
    
    def book_exists(self, book_id: int) -> bool:
        """
        Check if a book exists in the API.

        Args:
            book_id (int): The ID of the book to check.

        Returns:
            bool: True if the book exists, False otherwise.
        """
        existing_ids = self.get_existing_book_ids()
        return book_id in existing_ids
    
    def build_valid_book_data(self, random_book_id: int) -> Dict[str, Any]:
        """
        Build a valid book data object with optional overrides.

        Args:
            overrides (Optional[Dict[str, Any]]): A dictionary of fields to override in the default book data.

        Returns:
            BookClientConfig: The constructed book data object.
        """
        default_data = {
            "id": random_book_id,
            "title": f"Creating valid book randomic{random_book_id}",
            "description": f"Default Description for create book {random_book_id}",
            "pageCount": 100,
            "excerpt": f"This is a default excerpt. book randomic{random_book_id}",
            "publishDate": "2023-01-01T00:00:00Z"
        }
        return default_data
    