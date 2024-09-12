import os
from venv import logger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from .models import EncryptedFile
from .serializers import EncryptedFileSerializer
from utils.encryption import generate_key, encrypt_file
from dotenv import load_dotenv
import base64
import boto3

load_dotenv()


# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
)


class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = EncryptedFileSerializer(data=request.data)
            
            if serializer.is_valid():
                # Get file from request
                uploaded_file = request.FILES['file']
                file_data = uploaded_file.read()
                
                # Generate encryption key
                key = generate_key()
                
                # Encrypt file data
                encrypted_data = encrypt_file(key, file_data)
                

                # Encode the key using Base64
                encoded_key = base64.b64encode(key).decode('utf-8')
                
                # Define S3 bucket and file path
                bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
                s3_file_path = f"encrypted_files/{uploaded_file.name}"
                
                
                # Upload encrypted file to S3
                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=s3_file_path,
                    Body=encrypted_data
                )
                
                # Construct the URL of the uploaded file
                file_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_file_path}"
                
                print("stop here error")
                return Response({
                    'message': 'File uploaded and encrypted successfully!',
                    'file_url': file_url,
                    'encryption_key': encoded_key
                }, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error occurred uploading file: {e}")
            return Response({"detail": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
