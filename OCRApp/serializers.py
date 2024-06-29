from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import serializers
from .models import OCRImage


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user


class OCRImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRImage
        fields = ('id', 'image', 'extracted_text', 'bold_words', 'image_base64', 'created_at')
