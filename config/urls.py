from django.contrib import admin
from django.urls import path, include 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

# Project URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('token_endpoint.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
