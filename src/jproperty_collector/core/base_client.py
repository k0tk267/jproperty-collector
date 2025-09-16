import requests
from requests.adapters import HTTPAdapter
from urllib.parse import urlencode
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
)
from  typing import Any
from .exceptions import APIError
import gzip
import json

class BaseHTTPClient:
    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        timeout: int = 30,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0
    ):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.session = requests.Session()
        
        adapter = HTTPAdapter()
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def _prepare_headers(self) -> dict[str, str]:
        headers = {
            'User-Agent': 'jproperty-collector/0.1.0',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate'
        }
        
        if self.api_key:
            headers['Ocp-Apim-Subscription-Key'] = self.api_key
            
        return headers
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        if params:
            params = {k: v for k, v in params.items() if v is not None}
            url += f"?{urlencode(params)}"
        
        headers = self._prepare_headers()
        
        try:
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            return self._handle_response(response)
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")
    
    def _handle_response(self, response: requests.Response) -> dict[str, Any]:
        if response.status_code >= 400:
            raise APIError(
                f"API request failed: {response.status_code}",
                status_code=response.status_code
            )
        
        content = response.content
        if response.headers.get('Content-Encoding') == 'gzip':
            content = gzip.decompress(content)
        
        try:
            return json.loads(content.decode('utf-8'))
        except json.JSONDecodeError as e:
            raise APIError(f"Failed to parse JSON response: {str(e)}")
