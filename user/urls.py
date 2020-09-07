from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register-user'),
    path('token/', views.CustomObtainToken.as_view(), name='obtain-token'),
    path('profile/', views.RetrieveUpdateUser.as_view(), name='profile')
]
