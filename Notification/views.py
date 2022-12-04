from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render,  get_object_or_404
from .models import WelcomeNotification, CommentNotification
from rest_framework.views import APIView
from . import serializers

class WelcomeNotificationView(APIView):

    def get(self,request,pk):
        notification=WelcomeNotification.objects.get(id=pk)
        serializer=serializers.WelcomeNotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self,request,pk):
        notification=get_object_or_404(WelcomeNotification, id=pk)
        if notification.user==request.user:
            notification.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class CommentNotificationView(APIView):

    def get(self,request,pk):
        notification=CommentNotification.objects.get(id=pk)
        serializer=serializers.CommentNotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self,request,pk):
        notification=get_object_or_404(CommentNotification, id=pk)
        if notification.post_user==request.user:
            notification.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class MyCommentNotificationList(APIView):

    def get(self,request): #get all my comment notifications
        notification=CommentNotification.objects.filter(post_user=request.user)
        serializer=serializers.CommentNotificationSerializer(notification, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
