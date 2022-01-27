from django.contrib import admin

from . import models


@admin.register(models.BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'first_name', 'last_name','phone')


@admin.register(models.Product)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'price', 'approved1','closed','opened','pending','declined')