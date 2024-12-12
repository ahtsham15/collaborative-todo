from rest_framework import generics
from rest_framework.permissions import AllowAny
from tasks.serializers import RegisterSerializer, LoginSerializer
# from django.contrib.auth.models import User
from tasks.models.userModel import User
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from tasks.serializers import UserSerializer 
from rest_framework.response import Response
from rest_framework import status

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                user = user
            else:
                user = None
        except User.DoesNotExist:
            user = None
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                "status": "success",
                "data": {
                    "user":user_serializer.data,
                    "refresh":str(refresh),
                    "access":str(refresh.access_token)
                }
            },status=status.HTTP_200_OK)
        else:
            return Response({
                "status": False,
                "message": "Invalid credentials"
            },status=status.HTTP_401_UNAUTHORIZED)
