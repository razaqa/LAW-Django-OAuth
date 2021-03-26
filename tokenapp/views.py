from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from tokenapp.constants import ErrorMessage
from tokenapp.serializers import TokenAPISerializer
from tokenapp.response import error_response

class TokenAPIView(APIView):
    def post(self, request):
        serializer = TokenAPISerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        if serializer.error_messages == ErrorMessage.FAILED_AUTHENTICATION.value:
            return Response(
                error_response('Not Found', serializer.error_messages),
                status=status.HTTP_404_NOT_FOUND
            )
        if serializer.error_messages == ErrorMessage.INVALID_GRANT_TYPE.value:
            return Response(
                error_response('Unprocessable Entity', serializer.error_messages),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        if serializer.error_messages == ErrorMessage.INVALID_CLIENT_APP.value:
            return Response(
                error_response('Not Found', serializer.error_messages),
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            error_response('Bad Request', serializer.error_messages),
            status=status.HTTP_400_BAD_REQUEST
        )

