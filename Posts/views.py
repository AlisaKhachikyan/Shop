from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import Http404

Get_response_schema={
    status.HTTP_200_OK:openapi.Response('OK')
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


class AllCategories(APIView):

    @swagger_auto_schema(responses=Get_response_schema)
    def get(self, request):
        categories=models.Categories.objects.all()
        serializer=serializers.AllCategoriesSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetPost(APIView):

    @swagger_auto_schema(responses=Get_response_schema)
    def get(self, request, pk):
        instance=get_object_or_404(models.Post, id=pk)
        serializer=serializers.OnePostSerializer(instance)
        return Response(serializer.data)


class AddPost(APIView):
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(request_body=serializers.OnePostSerializer, responses=Add_response_schema)
    def post(self, request):
        serializer=serializers.OnePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #serializer.errors returns the correspondent error


class EditPost(APIView):
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(request_body=serializers.OnePostSerializer, responses=Edit_response_schema)
    def patch(self, request, pk):
        instance=get_object_or_404(models.Post, id=pk)
        if request.user==instance.user:
            serializer=serializers.OnePostSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class DeletePost(APIView):

    @swagger_auto_schema(request_body=serializers.OnePostSerializer, responses=Delete_response_schema)
    def delete(self, request, pk):
        post=get_object_or_404(models.Post, id=pk)
        if post.user==request.user:  #check whether it is the user who posted it
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class AllComments(APIView):

    @swagger_auto_schema(responses=Get_response_schema)
    def get(self, request):
        comments=models.Comments.objects.all()
        serializer=serializers.GetCommentsSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddComment(APIView):
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(request_body=serializers.CommentSerializer, responses=Add_response_schema)
    def post(self, request):
        serializer=serializers.CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditComment(APIView):

    @swagger_auto_schema(request_body=serializers.CommentSerializer, responses=Edit_response_schema)
    def patch(self, request, pk):
        instance=get_object_or_404(models.Comments, id=pk)
        #post=instance.post
        if request.user==instance.user:
            serializer=serializers.CommentSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(user=request.user)
                #sendcommentnotification(msg='request.user commencted your post', post.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class DeleteComment(APIView):

    @swagger_auto_schema(request_body=serializers.CommentSerializer, responses=Delete_response_schema)
    def delete(self, request, pk):
        instance=get_object_or_404(models.Comments, id=pk)
        post=instance.post
        if request.user==instance.user or request.user==post.user:  #check whether it is the user who posted or commented it
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

#AVELACNEL COMMENTI VIEW
#tester posti hamar
#docker
#vonca notification ashxatum djangoum, vonc chat sarqel
