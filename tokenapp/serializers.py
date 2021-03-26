from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from tokenapp.constants import ErrorMessage
from tokenapp.models import (
    Application,
    Token,
    UserInfo,
)
import binascii, os

class TokenAPISerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, write_only=True)
    password = serializers.CharField(max_length=40, write_only=True)
    grant_type = serializers.CharField(max_length=40, write_only=True)
    client_id = serializers.CharField(max_length=200, write_only=True)
    client_secret = serializers.CharField(max_length=200, write_only=True)

    access_token = serializers.CharField(read_only=True)
    expires_in = serializers.IntegerField(read_only=True)
    token_type = serializers.CharField(read_only=True)
    scope = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    def generate_key(self, length):
        return binascii.hexlify(os.urandom(length)).decode()
    
    def token_data(self):
        minutes_to_add = 5
        now = datetime.now()
        return {
            'access_token': self.generate_key(40),
            'expires_in': 60*minutes_to_add,
            'token_type': 'Bearer',
            'expired_date': now + timedelta(minutes = minutes_to_add),
            'scope': None,
            'refresh_token': self.generate_key(40),
        }

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        grant_type = data.get('grant_type')
        client_id = data.get('client_id')
        client_secret = data.get('client_secret')

        try:
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError(
                    ErrorMessage.FAILED_AUTHENTICATION.value
                )

            Application.objects.get(client_id=client_id, client_secret=client_secret)

            if grant_type == 'password':
                return data
            else:
                raise serializers.ValidationError(
                    ErrorMessage.INVALID_GRANT_TYPE.value
                )
        except Application.DoesNotExist:
            raise serializers.ValidationError(
                ErrorMessage.INVALID_CLIENT_APP.value
            )

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        client_id = validated_data['client_id']
        client_secret = validated_data['client_secret']

        try:
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError(
                    ErrorMessage.FAILED_AUTHENTICATION.value
                )
            application = Application.objects.get(client_id=client_id, client_secret=client_secret)
            token_data = self.token_data()

            Token.objects.create(
                user = user,
                application = application,
                access_token = token_data['access_token'],
                expired_date = token_data['expired_date'],
                token_type = token_data['access_token'],
                scope = token_data['scope'],
                refresh_token = token_data['refresh_token']
            )

            token_data.pop('expired_date')
            return token_data

        except Application.DoesNotExist:
            raise serializers.ValidationError(
                ErrorMessage.INVALID_CLIENT_APP.value
            )
