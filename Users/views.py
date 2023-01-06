from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models
from . import serializers
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


Get_response_schema={
    status.HTTP_200_OK:openapi.Response('OK'),
    status.HTTP_400_BAD_REQUEST:openapi.Response('Not Valid'),
    status.HTTP_401_UNAUTHORIZED:openapi.Response('Unauthorized')
}

Add_response_schema={
    status.HTTP_201_CREATED:openapi.Response('Posted'),
    status.HTTP_400_BAD_REQUEST:openapi.Response('Not Valid')
}

Edit_response_schema={
    status.HTTP_201_CREATED:openapi.Response('Edited'),
    status.HTTP_400_BAD_REQUEST:openapi.Response('Not Valid'),
    status.HTTP_401_UNAUTHORIZED:openapi.Response('Unauthorized')
}

Delete_response_schema={
    status.HTTP_204_NO_CONTENT:openapi.Response('Deleted'),
    status.HTTP_401_UNAUTHORIZED:openapi.Response('Unauthorized')
}


class AllUsers(APIView):
    @swagger_auto_schema(responses=Get_response_schema)
    def get(self, request):
        users=models.CustomUser.objects.all()
        serializer=serializers.AllUsersSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class User(APIView):
    @swagger_auto_schema(responses=Get_response_schema)
    def get(self, request, pk): #get user with id
        serializer=serializers.UserSerializer(models.CustomUser.objects.get(id=pk))
        return Response(serializer.data)


class MyUser(APIView):
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(responses=Get_response_schema)
    def get(self,request): #get yourself as a user
        serializer=serializers.UserSerializer(models.CustomUser.objects.get(id=request.user.id))
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializers.UserSerializer, responses=Edit_response_schema)
    def patch(self,request): #change your info
        instance=get_object_or_404(models.CustomUser.objects.all(),pk=request.user.id)
        serializer=serializers.UserSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

class RegisterView(APIView):
    @swagger_auto_schema(request_body=serializers.RegisterSerializer, responses=Add_response_schema)
    def post(self,request):
        serializer=serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SearchUser(APIView):
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(responses=Get_response_schema)
    def get(self, request, format=None, *args, **kwargs):
        get_data=request.query_params
        users=models.CustomUser.objects.all()
        if get_data:
            if get_data.get('first_name'):
                users=models.CustomUser.objects.filter(first_name__icontains=get_data['first_name'])
            elif get_data.get('last_name'):
                users=models.CustomUser.objects.filter(last_name__icontains=get_data['last_name'])
            elif get_data.get('email'):
                users=models.CustomUser.objects.filter(email__icontains=get_data['email'])
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer=serializers.AllUsersSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
