from django.db import models
from cities_light.models import City
from django.contrib.auth import get_user_model


class User(models.Model):
    Tuser_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=32, null=True, blank=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    phone = models.CharField(max_length=15)
    age = models.PositiveIntegerField(default=0)
    gender = models.CharField(max_length=10, default='Other')
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)

    is_bot = models.BooleanField(default=False)
    language_code = models.CharField(max_length=10, default='am')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # return f'@{self.username}' if self.username is not None else f'{self.Tuser_id}'
        return str(self.Tuser_id)


class BotUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=32, null=True, blank=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    #####
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    location = models.CharField(max_length=33)
    phone = models.CharField(max_length=15)

    """user_model = get_user_model()
    user_model.add_to_class('following',models.ManyToManyField('self',
                                                       through=Likes,
                                       related_name='followers',symmetrical=False))"""
    def __str__(self):
     return str(self.user_id)


class Likes(models.Model):
    user_from = models.ForeignKey(BotUser, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(BotUser, related_name='rel_to_set', on_delete=models.CASCADE)
    like = models.ManyToManyField(BotUser)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_from} Liked {self.user_to}'


class Profile(models.Model):
    buser = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    location = models.CharField(max_length=22)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=00)
    chat_id = models.IntegerField(default=0)
    message_id = models.IntegerField()
    text = models.CharField(max_length=4096)

    # fn = user.first_name

    def __str__(self):
        return str(self.user.first_name)
