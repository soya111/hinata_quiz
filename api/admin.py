from django.contrib import admin
from .models import Quiz, Choice, Nonce, UserInfo

# Register your models here.

admin.site.register(Quiz)
admin.site.register(Choice)
admin.site.register(Nonce)
admin.site.register(UserInfo)
