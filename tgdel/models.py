from django.db import models
from django.utils.timezone import now
 

class BotUser(models.Model):
    """
    The bot user
    """

    # Basic data
    chat_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Permissions
    is_admin = models.BooleanField(default=False)

    # State
    has_blocked_bot = models.BooleanField(default=False)
    last_action_datetime = models.DateTimeField(null=True, blank=True)

    language = models.CharField(max_length=2, choices=(
        # define your bot languages here
        ('ES', 'es'),
        ('EN', 'en'),
    ), default=None, null=True, blank=True)

    def __str__(self):
        
        return str(self.chat_id)

    def report_last_action(self):
        self.last_action_datetime = now()
