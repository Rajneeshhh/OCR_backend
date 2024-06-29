from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import base64
import pytesseract
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import OCRImage
from .serializers import OCRImageSerializer

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Rajneesh\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

class OCRImageView(APIView):
    def post(self, request):
        image = request.FILES.get('image')
        if not image:
            return Response({'error': 'No image data provided'}, status=status.HTTP_400_BAD_REQUEST)

        img = Image.open(image)
        extracted_text = pytesseract.image_to_string(img).strip()
        # print(extracted_text)
        bold_words = [word for word in extracted_text.split() if word.isupper()]

        image_base64 = base64.b64encode(image.read()).decode('utf-8')

        ocr_image = OCRImage(
            image_base64=image_base64,
            extracted_text=extracted_text,
            bold_words=', '.join(bold_words)
        )
        ocr_image.save()

        serializer = OCRImageSerializer(ocr_image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'user': serializer.data, 'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
