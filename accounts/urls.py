from django.urls import path
from .views import RegisterView, LoginView, RefreshView, LogoutView, MeView

urlpatterns = [
    path("signup/", RegisterView.as_view(), name="signup"),
    path("login/",  LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", MeView.as_view(), name="me"),
]
