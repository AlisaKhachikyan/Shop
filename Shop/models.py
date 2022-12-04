from django.db import models
from Users.models import CustomUser as User

class Merchandise(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    category=models.CharField(max_length=25)
    condition=models.CharField(max_length=50)
    description=models.TextField()
    price=models.FloatField()
    title=models.CharField(max_length=20)
    image=models.ImageField(upload_to=None, null=True, blank=True)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    active=models.BooleanField(default=True)

    def __str__(self):
        return self.user.email

class CartItem(models.Model):
    merchandise=models.ForeignKey(Merchandise, on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)
    price=models.FloatField()

    def __str__(self):
        return self.merchandise.title
