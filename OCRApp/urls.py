from django.urls import path
from .views import OCRImageView
from .views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('upload/', OCRImageView.as_view(), name='upload_image'),
]
