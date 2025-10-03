from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# --- Pages ---
class HomePage(TemplateView):
    template_name = "index.html"

class LoginPage(TemplateView):
    template_name = "login.html"

class BanyaPage(TemplateView):
    template_name = "banya_base.html"

class CafePage(TemplateView):
    template_name = "cafe.html"

# --- API ---
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = (request.data.get("username") or "").strip()
        password = request.data.get("password") or ""
        if not username or not password:
            return Response({"detail": "Введите логин и пароль"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"detail": "Неверный логин или пароль"}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)  # сессия
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)
