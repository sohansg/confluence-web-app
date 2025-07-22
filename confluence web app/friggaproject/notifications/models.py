
from django.db import models
from users.models import User
from documents.models import Document

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.recipient.email} - {self.message[:40]}"


# Create your models here.
