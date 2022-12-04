from rest_framework import serializers
from . import models


class AllCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Categories
        fields=['name', 'description']

# class AllCommentsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=models.Comments
#         fields=['post','content']

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model=models.Comments
        fields=['content','post','user',]


class GetCommentsSerializer(serializers.ModelSerializer):
    post=serializers.SerializerMethodField()

    class Meta:
        model=models.Comments
        fields=['content','user','post']
    def get_post(self,obj):
        post=models.Post.objects.filter(content=obj)
        return OnePostSerializer(obj.post).data['title']


class OnePostSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Post
        fields=['title', 'content', 'user']
