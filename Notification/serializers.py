from rest_framework import serializers
from . import models
from Posts.models import Comments


class WelcomeNotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=models.WelcomeNotification
        fields=["title", "msg"]


class CommentSerializer_(serializers.ModelSerializer): #CommentSerializer for CommentNotification

    class Meta:
        model=Comments
        fields=['content']

class CommentNotificationSerializer(serializers.ModelSerializer):
    comment=serializers.SerializerMethodField()

    class Meta:
        model=models.CommentNotification
        fields=["comment", "msg", "is_seen", "datetime"]

    def get_comment(self, obj):
        return CommentSerializer_(obj.comment).data
