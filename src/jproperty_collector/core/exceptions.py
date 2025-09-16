class JPropertyCollectorError(Exception):
    pass

class ValidationError(JPropertyCollectorError):
    pass

class APIError(JPropertyCollectorError):
    def __init__(self, message: str, status_code: int | None = None, response_data: dict | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data

class AuthenticationError(APIError):
    pass

class RateLimitError(APIError):
    pass
