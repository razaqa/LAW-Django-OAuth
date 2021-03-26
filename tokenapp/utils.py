from datetime import datetime
from tokenapp.models import Token
import pytz

def get_bearer_token(request):
    auth_header = request.headers.get('Authorization')
    if auth_header == None:
        return None
    
    auth_type = auth_header.split(' ')[0]
    if auth_type != 'Bearer':
        return None

    auth_token = auth_header.split(' ')[1]
    return auth_token

def authenticate_token(access_token):
    try:
        token = Token.objects.get(access_token=access_token)
        now = datetime.now().replace(tzinfo=pytz.UTC)
        if (now < token.expired_date):
            return token
        return None
    except Token.DoesNotExist:
        return None