from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from tokenapp.constants import ErrorMessage
from tokenapp.models import UserInfo
from tokenapp.serializers import TokenAPISerializer
from tokenapp.response import error_response
from tokenapp.utils import (
    get_bearer_token,
    authenticate_token,
)

class TokenAPIView(APIView):
    def post(self, request):
        serializer = TokenAPISerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        try:
            serializer.errors['non_field_errors'][0]
        except Exception as e:
            return Response(
                error_response('Bad Request', serializer.errors),
                status=status.HTTP_400_BAD_REQUEST
            )

        if serializer.errors['non_field_errors'][0] == ErrorMessage.FAILED_AUTHENTICATION.value:
            return Response(
                error_response('Not Found', serializer.errors['non_field_errors'][0]),
                status=status.HTTP_404_NOT_FOUND
            )
        elif serializer.errors['non_field_errors'][0] == ErrorMessage.INVALID_GRANT_TYPE.value:
            return Response(
                error_response('Unprocessable Entity', serializer.errors['non_field_errors'][0]),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        elif serializer.errors['non_field_errors'][0] == ErrorMessage.INVALID_CLIENT_APP.value:
            return Response(
                error_response('Not Found', serializer.errors['non_field_errors'][0]),
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            return Response(
                error_response('Bad Request', serializer.errors),
                status=status.HTTP_400_BAD_REQUEST
            )

class ResourceAPIView(APIView):
    def post(self, request):     
        access_token = get_bearer_token(request)
        if access_token == None:
            return Response(
                error_response('Unauthorized', ErrorMessage.INVALID_TOKEN.value),
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token = authenticate_token(access_token)
        if token == None:
            return Response(
                error_response('Unauthorized', ErrorMessage.INVALID_TOKEN.value),
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        profile = {}
        try:
            user_info = UserInfo.objects.get(user=token.user)
            profile['full_name'] = user_info.full_name
            profile['npm'] = user_info.npm
        except UserInfo.DoesNotExist:
            profile['full_name'] = None
            profile['npm'] = None

        response = {
            'access_token': token.access_token,
            'client_id': token.application.client_id,
            'user_id': token.user.username,
            'full_name': profile['full_name'],
            'npm': profile['npm'],
            'expires': token.expired_date,
            'refresh_token': token.refresh_token,
        }
        return Response(
            response,
            status=status.HTTP_200_OK
        )
