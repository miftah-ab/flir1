from django.db import models


class BotUser(models.Model):
    user_id = models.CharField(max_length=20)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15, null=True, blank=True)
    username = models.CharField(max_length=15, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return str(self.user_id)


class Product(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, null=True)
    category = models.CharField(max_length=15)
    title = models.CharField(max_length=100)
    price = models.CharField(max_length=15)
    description = models.CharField(max_length=1000)
    ####

    closed = models.BooleanField(default=False)  # BY USER after selling
    #approved = models.BooleanField(null=True, blank=True) # only for admin
    approved1 = models.BooleanField(default=None)
    declined = models.BooleanField(default=False) # only for admin
    pending = models.BooleanField(default=True)  # if approved chenged it change
    opened = models.BooleanField(default=True) # all except closed   or approved true

    def __str__(self):
        return f'{self.category} {self.title}'
