from django.test import TestCase, Client
from django.urls import reverse, resolve
from rest_framework.test import APIClient, APITestCase
from Users import models
from Users.serializers import AllUsersSerializer, UserSerializer, RegisterSerializer
from collections import OrderedDict
from rest_framework_simplejwt.tokens import RefreshToken


class UsersTest(APITestCase):
    def setUp(self):
        self.user_1=models.CustomUser.objects.create_user(email='fdgjfd@mail.ru', password='onetwofive', first_name='A', last_name='K')
        self.user_2=models.CustomUser.objects.create_user(email='fdgjgrfd@mail.ru', password='twofive', first_name='L', last_name='M')
        self.user_3=models.CustomUser.objects.create_user(email='fdgbfjfd@mail.ru', password='onefive', first_name='M', last_name='K')
        self.c=Client()
        login=self.c.login(email='fdgjfd@mail.ru',password='onetwofive')
        self.refresh=RefreshToken.for_user(self.user_1)

    def test_user_get(self): #get yourself as user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response=self.client.get(reverse('myuser'))
        response_data=response.data
        serializer_data=UserSerializer(self.user_1).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer_data,response_data)

    def test_user_get_pk(self): #get yourself as user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response=self.client.get(reverse('oneuser', args=[1]))
        response_data=response.data
        serializer_data=UserSerializer(self.user_1).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer_data,response_data)
#
    def test_all_users_get(self):
        response=self.client.get(reverse('allusers'))
        response_data=response.data
        serializer_data=[OrderedDict(AllUsersSerializer(self.user_1).data),
        OrderedDict(AllUsersSerializer(self.user_2).data),
        OrderedDict(AllUsersSerializer(self.user_3).data)]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer_data,response_data)

    def test_myuser_patch(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response=self.client.patch(reverse('myuser'), {'first_name':'Ann'})
        response_data=response.data
        patch_user=models.CustomUser.objects.get(id=1)
        serializer=UserSerializer(patch_user)
        serializer_data=serializer.data
        self.assertEqual(response_data,serializer_data)

    def test_searchuser_by_first_name(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response=self.client.get(reverse('searchuser'),{'first_name':'A'})
        response_data=response.data
        user=models.CustomUser.objects.get(first_name='A')
        serializer_data=[OrderedDict(AllUsersSerializer(user).data)]
        self.assertEqual(response_data, serializer_data)
        self.assertEqual(response.status_code, 200)

    def test_searchuser_by_last_name(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response=self.client.get(reverse('searchuser'),{'last_name':'M'})
        response_data=response.data
        user=models.CustomUser.objects.get(last_name='M')
        serializer_data=[OrderedDict(AllUsersSerializer(user).data)]
        self.assertEqual(response_data, serializer_data)
        self.assertEqual(response.status_code, 200)

    def test_searchuser_by_email(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response=self.client.get(reverse('searchuser'),{'email':'fdgjfd@mail.ru'})
        response_data=response.data
        user=models.CustomUser.objects.get(email='fdgjfd@mail.ru')
        serializer_data=[OrderedDict(AllUsersSerializer(user).data)]
        self.assertEqual(response_data, serializer_data)
        self.assertEqual(response.status_code, 200)

    def test_searchuser_wrong_get_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response=self.client.get(reverse('searchuser'),{'emaill':'hfhbfxg'})
        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, 400)

class RegisterTest(APITestCase):
    def test_registerview(self):    #comparing to queryset get
        post_response=self.client.post(reverse('register'), {'email' : 'hiuuygu@mail.ru',
                                                                'first_name':'Paul',
                                                                'last_name':'Akm',
                                                                'password': '778778455h',
                                                                'password2':'778778455h'})
        post_response_data=post_response.data
        registered_user=models.CustomUser.objects.get(email='hiuuygu@mail.ru')
        serializer_data=AllUsersSerializer(registered_user).data
        self.assertEqual(post_response_data, serializer_data)
        self.assertEqual(post_response.status_code, 201)
