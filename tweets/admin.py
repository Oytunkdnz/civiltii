from django.contrib import admin
from tweets.models import User, Tweet


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name"]


class TweetAdmin(admin.ModelAdmin):
    list_display = ["author", "text", "created"]

admin.site.register(User, UserAdmin)
admin.site.register(Tweet, TweetAdmin)
