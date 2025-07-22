from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Document(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    content = models.TextField()
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)  # renamed from last_modified

    def __str__(self):
        return f"Document {self.id} by {self.author.email}"


class SharedDocument(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='shared_entries')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_with_me')
    can_edit = models.BooleanField(default=False)
    shared_at = models.DateTimeField(default=timezone.now)  # added this field recently

    def __str__(self):
        return f"{self.document.id} shared with {self.shared_with.email}"
