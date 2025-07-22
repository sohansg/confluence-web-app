from rest_framework import serializers
from .models import Document, SharedDocument
from users.models import User
from .utils import handle_user_mentions


# ✅ Document Serializer
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['author']

    def create(self, validated_data):
        document = Document.objects.create(**validated_data)
        handle_user_mentions(document)
        return document

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        handle_user_mentions(instance)
        return instance


# ✅ Share Document Serializer with can_edit
class ShareDocumentSerializer(serializers.ModelSerializer):
    shared_with_email = serializers.EmailField(write_only=True)
    can_edit = serializers.BooleanField(default=False)

    class Meta:
        model = SharedDocument
        fields = ['shared_with_email', 'can_edit']

    def validate_shared_with_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email.")
        return user

    def create(self, validated_data):
        document = self.context['document']
        shared_with_user = validated_data['shared_with_email']
        can_edit = validated_data.get('can_edit', False)

        return SharedDocument.objects.create(
            document=document,
            shared_with=shared_with_user,
            can_edit=can_edit
        )
