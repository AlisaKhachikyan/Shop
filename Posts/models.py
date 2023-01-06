from django.db import models
from Users.models import CustomUser as User


class Categories(models.Model):
    name=models.CharField(max_length=250)
    description=models.TextField()

    def __str__(self):
        return self.name


class Post(models.Model):
    category=models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, related_name="category")
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title=models.CharField(max_length=250)
    content=models.TextField()

    def __str__(self):
        return self.title


class Comments(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    content=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content
