from django.contrib import admin
from . import models


admin.site.register(models.Merchandise)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
# Register your models here.
