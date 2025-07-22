from django.urls import path
from .views import (
    DocumentListCreateView,
    DocumentDetailView,
    ShareDocumentView,
    SharedWithMeView,
)

urlpatterns = [
    # Create and list all documents
    path('', DocumentListCreateView.as_view(), name='document-list-create'),

    # Retrieve, update, delete a specific document by ID
    path('<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),

    # Share a document with another user
    path('<int:pk>/share/', ShareDocumentView.as_view(), name='share-document'),

    # View all documents shared with the logged-in user
    path('shared-with-me/', SharedWithMeView.as_view(), name='shared-with-me'),
]
