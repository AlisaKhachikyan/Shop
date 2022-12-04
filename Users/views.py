from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models
from . import serializers
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class AllUsers(APIView):

    def get(self, request):
        users=models.CustomUser.objects.all()
        serializer=serializers.CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class User(APIView):

    def get(self,request):
        serializer=serializers.UserSerializer(models.CustomUser.objects.get(id=request.user.id))
        return Response(serializer.data)

    def put(self,request):
        instance=get_object_or_404(models.CustomUser.objects.all(),pk=request.user.id)
        serializer=serializers.UserSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

class RegisterView(APIView):
    
    def post(self,request):
        serializer=serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
