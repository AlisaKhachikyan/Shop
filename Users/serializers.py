from rest_framework import serializers
from . import models
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.CustomUser
        fields=['first_name', 'last_name', 'email','date_joined','date_of_birth']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.CustomUser
        fields=['first_name', 'last_name', 'email','date_joined','date_of_birth']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.CustomUser
        fields = ['email','first_name','last_name', 'password', 'password2']
        extra_kwargs = {
            # 'password':{'write_only': True},
            # 'password_2':{'write_only': True}, #password 2-y chexav fieldsi mej grel, Field name `password2` is not valid for model `CustomUser`.
            'first_name':{'required': True},
            'last_name':{'required': True},
        }

    def validate(self, attrs):
        print(attrs)
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs #??


    def create(self, validated_data):
        print(validated_data)
        user = models.CustomUser.objects.create_user(
        email=validated_data['email'],  #tarberuyuny erb vor email= chem grum, **extra_fields
        password=validated_data['password'],
        last_name=validated_data['last_name'],
        first_name=validated_data['first_name'])
        user.save()
        return user



#registerserializer..view Postov USER create ..create user funkcia u ogtagorcuma validated data
