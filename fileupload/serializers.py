from rest_framework import serializers
from .models import EncryptedFile



class EncryptedFileSerializer(serializers.Serializer):
    class Meta:
        model = EncryptedFile
        fields = ['file']
