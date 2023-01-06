from rest_framework import serializers
from . import models
from django.db.models import Sum

class AllMerchandisesSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Merchandise
        fields=['category','condition','price', 'title']

class MerchandiseSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Merchandise
        fields=['category','condition','price', 'title', 'description', 'image']

class CartItemsListSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Merchandise
        fields=['pk','category','condition','price', 'title']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.CartItem
        fields=['merchandise']

class OwnCartItem(serializers.ModelSerializer):
    merchandise=serializers.SerializerMethodField()
    
    class Meta:
        model=models.CartItem
        fields=['pk','merchandise', 'price']

    def get_merchandise(self, obj):
        return MerchandiseSerializer(obj.merchandise).data #CartItem model mechandise

class CartSerializer(serializers.ModelSerializer):
    cart_merchandise=serializers.SerializerMethodField()
    total_price=serializers.SerializerMethodField()

    class Meta:
        model=models.Cart
        fields=['pk', 'cart_merchandise', 'total_price', 'active']

    def get_cart_merchandise(self,obj):
        items=models.CartItem.objects.filter(cart=obj)  #obj is Cart
        return OwnCartItem(items, many=True).data

    def get_total_price(self,obj):
        return models.CartItem.objects.filter(cart=obj).aggregate(Sum('price'))['price__sum']
