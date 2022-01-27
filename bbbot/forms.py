from django import forms
from .models import User, Message


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('chat_id', 'message_id', 'text')
