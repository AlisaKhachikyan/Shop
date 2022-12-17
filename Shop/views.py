from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from . import models
from . import serializers
from Users.models import CustomUser as User
from django.http import Http404
from django.db.models import Q, CharField
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404

class AllMerchandises(APIView):
    def get(self, request, format=None, *args, **kwargs):
        get_data=request.query_params
        merchandises=models.Merchandise.objects.all()
        if get_data:
            if get_data.get('filter', '')=='newest':  #filter is a key, newest is a value
                merchandises=merchandises.order_by('-pk')
            elif get_data.get('filter', '')=='lowest price':
                merchandises=merchandises.order_by('price')
            elif get_data.get('filter', '')=='alphabetical':
                merchandises=merchandises.order_by('-title')
            elif get_data.get('filter', '')=='by user':
                merchandises=merchandises.filter(user=get_data.get('user')) ##we need to input user ID, as user in Merchandise model is a foreign key
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer=serializers.AllMerchandisesSerializer(merchandises, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SearchMerchandise(APIView):
    def get(self, request, format=None, *args, **kwargs):
        get_data=request.query_params
        all_merchandises=models.Merchandise.objects.all()
        if get_data:
            if get_data.get('title', ''):
                merchandise=models.Merchandise.objects.filter(title__icontains=get_data['title'])
                serializer=serializers.AllMerchandisesSerializer(merchandise, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif get_data.get('all', ''):
                fields=[f for f in models.Merchandise._meta.fields if isinstance(f, CharField)] #_meta.fields-Retrieve all field instances of a model
                queries=[Q(**{f.name+'__icontains': get_data.get('all')}) for f in fields] #dictionary
                qs=Q()
                for query in queries:
                    qs=qs|query
                merchandise=models.Merchandise.objects.filter(qs)
                serializer=serializers.AllMerchandisesSerializer(merchandise, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif get_data.get('lower than price',''):
                p=int(get_data.get('lower than price'))
                merchandises=[merchandise for merchandise in all_merchandises if merchandise.price<=p]
                serializer=serializers.AllMerchandisesSerializer(merchandises, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif get_data.get('higher than price',''):
                p=int(get_data.get('higher than price'))
                merchandises=[merchandise for merchandise in all_merchandises if merchandise.price>=p]
                serializer=serializers.AllMerchandisesSerializer(merchandises, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif get_data.get('only with picture',''):
                if get_data.get('only with picture','')=='Yes':
                    merchandises=[merchandise for merchandise in all_merchandises if merchandise.image]
                    serializer=serializers.AllMerchandisesSerializer(merchandises, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer=serializers.AllMerchandisesSerializer(all_merchandises, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserMerchandise(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        merchandises=models.Merchandise.objects.filter(user=request.user)
        serializer=serializers.AllMerchandisesSerializer(merchandises, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK )


    def patch(self, request, pk):  #patch for the merchandise, when the request user is the merchandise owner
        merchandise=models.Merchandise.objects.get(id=pk)
        if merchandise.user==request.user:
            serializer=serializers.MerchandiseSerializer(merchandise, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Merchandise(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, pk):
        merchandise=models.Merchandise.objects.get(id=pk)
        serializer=serializers.MerchandiseSerializer(merchandise)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #@swagger_auto_schema(request_body=serializers.MerchandiseSerializer)
    def post(self, request):
        serializer=serializers.MerchandiseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCartItem(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        try:
            cart=models.Cart.objects.get(user=request.user, active=True)
        except:
            cart=models.Cart.objects.create(user=request.user)
        merchandise=models.Merchandise.objects.get(id=request.data.get('merchandise'))  #dict.get()..requestum talis enq merchandise vorpes key u id-n vorpes value
        price=merchandise.price
        serializer=serializers.CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart=cart, price=price)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetCart(APIView):
    permission_classes=[IsAuthenticated]

    def get_object(self, pk):
        try:
            return models.CartItem.objects.get(pk=pk)
        except models.CartItem.DoesNotExist:
            raise Http404

    def get(self, request):
        try:
            cart=models.Cart.objects.get(user=request.user)
        except:
            cart=models.Cart.objects.create(user=request.user)
        serializer=serializers.CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self,request,pk):
        item=self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeleteCart(APIView):
    permission_classes=[IsAuthenticated]

    def delete(self, request):
        cart=get_object_or_404(models.Cart, user=request.user)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeleteCartItem(APIView):
    permission_classes=[IsAuthenticated]

    def delete(self, request, pk):
        cart_item=get_object_or_404(models.CartItem, id=pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
