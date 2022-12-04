from django.contrib import admin
from . import models

admin.site.register(models.WelcomeNotification)
admin.site.register(models.CommentNotification)
# Register your models here.
