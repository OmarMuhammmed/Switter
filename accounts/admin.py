from django.contrib import admin
from .models import CustomUser as User , Profile
# Register your models here.

admin.site.register(User)
admin.site.register(Profile)

