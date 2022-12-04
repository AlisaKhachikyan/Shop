from django.db import models
from Posts.models import Post, Comments
from Users.models import CustomUser as User


class WelcomeNotification(models.Model):

    title= models.CharField(max_length=200)
    msg = models.TextField()
    is_seen = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CommentNotification(models.Model):

    msg = models.TextField()
    is_seen = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True )
    post_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='post_user')
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
