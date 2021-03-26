from django.contrib.auth.models import User
from django.db import models
import uuid

class Application(models.Model):
    client_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    client_name = models.CharField(max_length=200)
    client_secret = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.client_name

class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=40, unique=True)
    expired_date = models.DateTimeField()
    token_type = models.CharField(max_length=20)
    scope = models.CharField(max_length=20, blank=True, null=True)
    refresh_token = models.CharField(max_length=40)

    def __str__(self):
        return self.user.username

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    npm = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.npm