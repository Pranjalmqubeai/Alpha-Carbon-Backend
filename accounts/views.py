from django.contrib.auth.models import User
from rest_framework import generics, permissions,status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import RegisterSerializer, UserSerializer

# SimpleJWT views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

# --- Auth endpoints ---

class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class MeView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

# Customize token response to include user info (optional but handy)
class LoginView(TokenObtainPairView):
    """
    POST /api/auth/login/  { "username": "...", "password": "..." }
    Returns: access, refresh, and basic user info
    """
    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        if resp.status_code == 200 and request.user.is_authenticated is False:
            # If authentication succeeded, DRF won't set request.user;
            # get user by username
            try:
                user = User.objects.get(username=request.data.get("username"))
            except User.DoesNotExist:
                user = None
        else:
            user = request.user

        data = resp.data
        if user:
            data["user"] = UserSerializer(user).data
        resp.data = data
        return resp

class RefreshView(TokenRefreshView):
    """
    POST /api/auth/refresh/ { "refresh": "<refresh_token>" }
    Returns: new access (and if ROTATE_REFRESH_TOKENS=True, new refresh)
    """
    pass
class LogoutView(APIView):
    """
    POST /auth/logout/
    Body: { "refresh": "<refresh_token>" }
    Blacklists the given refresh token.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh)
            # If already blacklisted, .blacklist() raises TokenError; treat as already logged out
            token.blacklist()
            return Response({"detail": "Logged out."}, status=status.HTTP_200_OK)
        except TokenError as e:
            # Give a precise message: common cases are "Token is blacklisted" or "Token is invalid or expired"
            msg = str(e)
            if "blacklisted" in msg.lower():
                return Response({"detail": "Already logged out."}, status=status.HTTP_200_OK)
            return Response({"detail": "Invalid or expired refresh token."}, status=status.HTTP_400_BAD_REQUEST)