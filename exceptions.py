class APIException(Exception):
    """Custom exception class for handling API errors"""

    def __init__(self, message: str, status_code: int = 400):
        """Initialize the exception with a message and an optional status code"""
        self.message = message
        self.status_code = status_code
        super().__init__(message)
