from django.db import models


class EncryptedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    encrypted_key = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
