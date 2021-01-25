from django.urls import path, include
from .views import SessionView, CreateAuthUserView, AirplaneCollectorView
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

# APP URLs

router = routers.DefaultRouter()
router.register('token_endpoint', AirplaneCollectorView) # to get ALL current users GET /token_endpoint/

urlpatterns = [
    path('', include(router.urls)),
    path('create-user/', CreateAuthUserView.as_view(), name='create_user'),
    path('api/session-status/', SessionView.as_view(), name='session_status'),
]