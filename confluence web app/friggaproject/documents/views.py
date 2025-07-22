from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from .models import Document, SharedDocument
from .serializers import DocumentSerializer, ShareDocumentSerializer
from .utils import handle_user_mentions


# ✅ List and Create Documents
class DocumentListCreateView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        owned_docs = Document.objects.filter(author=user)
        shared_docs = Document.objects.filter(shared_entries__shared_with=user)
        return (owned_docs | shared_docs).distinct()

    def perform_create(self, serializer):
        document = serializer.save(author=self.request.user)
        handle_user_mentions(document)


# ✅ Retrieve, Update, Delete a Document with edit permission check
class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        document = super().get_object()
        user = self.request.user

        if document.author == user:
            return document

        shared_doc = SharedDocument.objects.filter(document=document, shared_with=user).first()
        if shared_doc:
            if self.request.method in ['GET', 'PUT', 'PATCH'] and (self.request.method == 'GET' or shared_doc.can_edit):
                return document

        raise PermissionDenied("You do not have access to this document.")

    def perform_update(self, serializer):
        document = serializer.save()
        handle_user_mentions(document)


# ✅ Share a Document with Another User (manual share with can_edit)
class ShareDocumentView(generics.CreateAPIView):
    serializer_class = ShareDocumentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            document = Document.objects.get(pk=pk, author=request.user)
        except Document.DoesNotExist:
            return Response({"error": "Document not found or not owned by you."}, status=404)

        # Check if already shared, update instead of duplicate
        existing = SharedDocument.objects.filter(
            document=document,
            shared_with__email=request.data.get('shared_with_email')
        ).first()

        if existing:
            existing.can_edit = request.data.get('can_edit', False)
            existing.save()
            return Response({
                "message": "Document sharing updated.",
                "shared_with": existing.shared_with.email,
                "can_edit": existing.can_edit
            }, status=200)

        serializer = self.get_serializer(data=request.data, context={'document': document})
        if serializer.is_valid():
            shared_instance = serializer.save()
            return Response({
                "message": "Document shared successfully!",
                "shared_with": shared_instance.shared_with.email,
                "can_edit": shared_instance.can_edit
            }, status=201)
        return Response(serializer.errors, status=400)


# ✅ View all documents shared with current user
class SharedWithMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            shared_docs = SharedDocument.objects.filter(shared_with=request.user)
            documents = [s.document for s in shared_docs if s.document]
            serializer = DocumentSerializer(documents, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
