import uuid
from django.core.exceptions import ValidationError
from django.db import models
from users.models import Profile
from django.utils.translation import gettext as _

class Message(models.Model):
    uid = models.UUIDField()
    content = models.TextField(blank=False)
    sender = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name="out_messages")
    sent_for = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name="in_messages")
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    STATUS = (
      ("sent",  _('Sent')),
      ("delivered", _('Delivered')),
      ("read", _('Read')),
    )
    status = models.CharField(choices=STATUS, default=STATUS[0][0], max_length=10)

    def clean(self):
        if hasattr(self, "sender") and hasattr(self, "sender"):
            if self.sender == self.sent_for:
                raise ValidationError("Sender and Receiver can't be same")

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Message, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.sender} to {self.sent_for}"

    @property
    def dated_on(self):
        return self.date


class Chat(models.Model):
    uid = models.UUIDField()
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="chats")
    chat_with = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name="chats_with")
    unread = models.PositiveIntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    messages = models.ManyToManyField(Message)

    class Meta:
        unique_together = ('owner', 'chat_with',)

    def __str__(self):
        return f"{self.owner}\'s chat with {self.chat_with}"


class A(models.Model):
    a = models.CharField(max_length=2)
