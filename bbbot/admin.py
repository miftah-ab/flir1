from django.contrib import admin
from .models import  User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'username', 'first_name', 'last_name',

        'created_at', 'updated_at',
    ]
    # list_filter = ["is_blocked_bot", "is_moderator"]
    search_fields = ('username', 'user_id')
