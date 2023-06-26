from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from users.views import ProfileUpdateView, RegisterView, generate_new_password
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/gennpassword', generate_new_password, name='generate_new_password'),
]
