from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from api.views import UserView, UserDetailView, OrderView, OrderDetailView, ChangePasswordView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('users/', UserView.as_view()),
    path('users/<int:pk>/', UserDetailView.as_view()),
    path('users/<int:pk>/change_password/', ChangePasswordView.as_view()),

    path('orders/', OrderView.as_view()),
    path('orders/<int:pk>/', OrderDetailView.as_view()),
]
