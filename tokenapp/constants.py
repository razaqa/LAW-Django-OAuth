from enum import Enum

class ErrorMessage(Enum):
    def __str__(self):
        return str(self.value)

    FAILED_AUTHENTICATION = 'Invalid username or password'
    INVALID_GRANT_TYPE = 'Invalid grant_type'
    INVALID_CLIENT_APP = 'Invalid client_id or client_secret'
    INVALID_TOKEN = 'Can\'t access due to invalid access_token'
