# source/client_api/config.py
from dataclasses import dataclass
from typing import Optional
import os


@dataclass(frozen=True)
class ClientAPIConfig:
    """
    Configuration for the Client API.

    Attributes:
        url_base (str): The base URL for the API server.
    """
    url_base: str
       
    @classmethod
    def from_env(cls, url_base: Optional[str] = None) -> 'ClientAPIConfig':
        """
        Create a ClientAPIConfig instance from environment variables.
        
        Args:
            url_base (Optional[str]): Optional URL base that overrides the environment variable.
                                      If not provided, uses CLIENT_API_URL_BASE env var or default.
        
        Returns:
            ClientAPIConfig: A new configuration instance.
        """
        # Se url_base foi fornecida, usa ela; senão pega do ambiente
        if url_base is None:
            url_base = os.getenv(
                "CLIENT_API_URL_BASE", 
                "https://fakerestapi.azurewebsites.net"
            )
        
        return cls(url_base=url_base.rstrip('/'))
