from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import RegisterView


app_name = 'myauth'

urlpatterns = [
    path('login/', 
         LoginView.as_view(template_name='myauth/login.html',
                           redirect_authenticated_user=True), 
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]