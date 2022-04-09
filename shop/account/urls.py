from django.contrib.auth import views
from django.urls import path

from .views import (ChangePassword, LoginUser, RegisterUser, UserDetail,
                    UserLogout)

app_name = 'account'

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('profile/', UserDetail.as_view(), name='profile'),
    path('changepassword/', ChangePassword.as_view(), name='changepassword'),
    path('password-change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
