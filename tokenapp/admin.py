from django.contrib import admin
from tokenapp.models import (
    Application,
    UserInfo,
    Token,
)

admin.site.register(Application)
admin.site.register(UserInfo)
admin.site.register(Token)