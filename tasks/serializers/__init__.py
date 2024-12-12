try:
    from .userSerializer import UserSerializer, LoginSerializer
except ImportError:
    from rest_framework import serializers
    # from django.contrib.auth.models import User
    from tasks.models.userModel import User
    from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password']

    def create(self, validated_data):
        user = User(
            username = validated_data['username'],
            email = validated_data['email'],
            password = make_password(validated_data['password'])
        )
        user.save()
        return user
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    # class Meta:
    #     model = User
