from django.contrib import admin
from .models import User, Message, Profile, BotUser,Likess


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'Tuser_id', 'username', 'first_name', 'last_name', 'phone', 'age', 'gender', 'lat', 'lon', 'language_code',

        'created_at', 'updated_at',
    ]
    # list_filter = ["is_blocked_bot", "is_moderator"]
    search_fields = ('username', 'Tuser_id')


@admin.register(BotUser)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'username', 'first_name','phone', 'last_name', 'age', 'gender', 'liked','liked_by','location'
    ]

#admin.site.register(Likes)

@admin.register(Likess)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user_from', 'user_to', 'like_id', 'liked', 'created'
    ]

@admin.register(Profile)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'buser', 'age', 'gender', 'location'
    ]


@admin.register(Message)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'text', 'chat_id', 'message_id'
    ]
