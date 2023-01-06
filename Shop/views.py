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
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
import logging


Get_response_schema={
    status.HTTP_200_OK:openapi.Response('OK'),
    status.HTTP_400_BAD_REQUEST:openapi.Response('Not Valid'),
}

Add_response_schema={
    status.HTTP_201_CREATED:openapi.Response('Posted'),
    status.HTTP_400_BAD_REQUEST:openapi.Response('Not Valid')
}

Edit_response_schema={
    status.HTTP_201_CREATED:openapi.Response('Edited'),
    status.HTTP_400_BAD_REQUEST:openapi.Response('Not Valid'),
    status.HTTP_401_UNAUTHORIZED:openapi.Response('Unauthorized')
}

Delete_response_schema={
    status.HTTP_204_NO_CONTENT:openapi.Response('Deleted'),
    status.HTTP_401_UNAUTHORIZED:openapi.Response('Unauthorized')
}


class AllMerchandises(APIView):

    @swagger_auto_schema(responses=Get_response_schema)
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

    @swagger_auto_schema(responses=Get_response_schema)
    def get(self, request, format=None, *args, **kwargs):
        get_data=request.query_params
        all_merchandises=models.Merchandise.objects.all()
        if get_data:
            if get_data.get('title', ''):
                merchandise=models.Merchandise.objects.filter(title__icontains=get_data['title'])
                serializer=serializers.AllMerchandisesSerializer(merchandise, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif get_data.get('all', ''):
                fields=[f for f in models.Merchandise._meta.fields if isinstance(f, CharField)] #_meta.fields-Retrieve all field instances of a model,, by CHarfield we except ID field
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

    @swagger_auto_schema(responses=Get_response_schema)
    def get(self, request):   #get your own merchandises
        merchandises=models.Merchandise.objects.filter(user=request.user)
        serializer=serializers.AllMerchandisesSerializer(merchandises, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK )

    @swagger_auto_schema(request_body=serializers.MerchandiseSerializer, responses=Edit_response_schema)
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

    @swagger_auto_schema(responses=Get_response_schema)
    def get(self, request, pk):
        merchandise=models.Merchandise.objects.get(id=pk)
        serializer=serializers.MerchandiseSerializer(merchandise)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializers.MerchandiseSerializer, responses=Add_response_schema)
    def post(self, request):
        logger=logging.getLogger('main')
        logger.info('New merchandise')
        serializer=serializers.MerchandiseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCartItem(APIView):
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(request_body=serializers.CartItemSerializer, responses=Add_response_schema)
    def post(self, request):
        try:
            cart=models.Cart.objects.get(user=request.user, active=True)
        except:
            cart=models.Cart.objects.create(user=request.user)
        merchandise=models.Merchandise.objects.get(id=request.data.get('merchandise'))  #dict.get().. merchandise is the key here
        price=merchandise.price
        serializer=serializers.CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart=cart, price=price)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetCart(APIView):
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(responses=Get_response_schema)
    def get(self, request): #get my cart
        try:
            cart=models.Cart.objects.get(user=request.user)
        except:
            cart=models.Cart.objects.create(user=request.user)  #if there is no cart, create it
        serializer=serializers.CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteCart(APIView):
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(request_body=serializers.CartSerializer, responses=Delete_response_schema)
    def delete(self, request):
        cart=get_object_or_404(models.Cart, user=request.user)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeleteCartItem(APIView):
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(request_body=serializers.CartItemSerializer, responses=Delete_response_schema)
    def delete(self, request, pk):
        cart_item=get_object_or_404(models.CartItem, id=pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
