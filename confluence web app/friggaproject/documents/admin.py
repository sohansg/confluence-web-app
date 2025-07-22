from django.contrib import admin
from .models import Document  # ✅ Only import Document

# ✅ Register Document model only
admin.site.register(Document)

# ❌ REMOVE or COMMENT OUT this if it's there:
# from .models import SharedDocument
# admin.site.register(SharedDocument)
