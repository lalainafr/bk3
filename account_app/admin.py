from django.contrib import admin

from account_app.models import Profile, User

admin.site.register(User)
admin.site.register(Profile)
