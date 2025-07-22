import re
from users.models import User
from .models import SharedDocument

def handle_user_mentions(document):
    """
    Scans the document content for @username mentions and shares the document
    with the mentioned users automatically (if they exist and are not the author).
    """
    # Use regex to find all @username patterns
    mentioned_usernames = set(re.findall(r'@(\w+)', document.content))

    for username in mentioned_usernames:
        try:
            user = User.objects.get(username=username)
            # Avoid re-sharing to the author
            if user != document.author:
                # Avoid duplicate sharing
                SharedDocument.objects.get_or_create(
                    document=document,
                    shared_with=user
                )
        except User.DoesNotExist:
            continue  # Skip users that don’t exist

