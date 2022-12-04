from django.test import TestCase, Client
from django.urls import reverse, resolve
from Shop.views import AllMerchandises, Merchandise
from Shop import models
from Users.models import CustomUser as User
from Shop.serializers import AllMerchandisesSerializer, MerchandiseSerializer
from rest_framework.test import APIClient, APITestCase
from collections import OrderedDict
import json
from django.db.models.query import QuerySet
from rest_framework_simplejwt.tokens import RefreshToken


class AllMerchandisesViewTest(APITestCase):
    def setUp(self):
        self.user_instance=User.objects.create_user(email='mmmkk@mail.ru', password='onetwofour', first_name='M', last_name='K')  #create_user-ov anel
        self.user_1=User.objects.create_user(email='fdgjfd@mail.ru', password='onetwofive', first_name='A', last_name='K')
        self.user_2=User.objects.create_user(email='fdfd@mail.ru', password='onetwofour', first_name='M', last_name='K')
        self.merchandise=models.Merchandise.objects.create(user=self.user_instance,
                                                            category='Electronics',
                                                            condition='good',
                                                            description='sdda',
                                                            price=5000,
                                                            title='Notebook')
        self.merchandise_1=models.Merchandise.objects.create(user=self.user_1,
                                                            category='Clothes',
                                                            condition='good',
                                                            description='sdda',price=4000,
                                                            title="dress")
        self.merchandise_2=models.Merchandise.objects.create(user=self.user_1,
                                                            category='Clothes',
                                                            condition='good',
                                                            description='sdda',
                                                            price=2000,
                                                            title="t-shirt")
        self.merchandise_3=models.Merchandise.objects.create(user=self.user_2,
                                                            category='Clothes',
                                                            condition='good',
                                                            description='sdda',
                                                            price=4000,
                                                            title="jeans")
        self.merchandise_4=models.Merchandise.objects.create(user=self.user_2,
                                                            category='Electronics',
                                                            condition='good',
                                                            description='sdda',
                                                            price=4000,
                                                            title="Computer")
    def test_allmerchandises_view_get(self):
        response=self.client.get(reverse('allmerchandises'))
        response_data=response.data
        serializer_data=[OrderedDict(AllMerchandisesSerializer(self.merchandise).data),
        OrderedDict(AllMerchandisesSerializer(self.merchandise_1).data),
        OrderedDict(AllMerchandisesSerializer(self.merchandise_2).data),
        OrderedDict(AllMerchandisesSerializer(self.merchandise_3).data),
        OrderedDict(AllMerchandisesSerializer(self.merchandise_4).data)]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer_data,response_data)


    def test_allmerchandises_view_filter_newest(self):
        response=self.client.get(reverse('allmerchandises'),{'filter':'newest'})
        response_data=response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data[0]['title'], 'Computer')
        self.assertEqual(response_data[1]['title'], 'jeans')

    def test_allmerchandises_view_filter_lowest_price(self):
        response=self.client.get(reverse('allmerchandises'),{'filter':'lowest price'})
        response_data=response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data[0]['price'], 2000)
        self.assertEqual(response_data[1]['price'], 4000)


class SearchMerchandiseViewTest(APITestCase):
    def setUp(self):
        self.user_1=User.objects.create_user(email='fdgjfd@mail.ru', password='onetwofive', first_name='A', last_name='K')
        self.user_2=User.objects.create_user(email='fdfd@mail.ru', password='onetwofour', first_name='M', last_name='K')
        self.user_1.save()
        self.c=Client()
        login=self.c.login(email='fdgjfd@mail.ru',password='onetwofive')
        #print(login)
        self.merchandise_1=models.Merchandise.objects.create(user=self.user_1,
                                                            category='Clothes',
                                                            condition='good',
                                                            description='sdda',price=4000,
                                                            title="dress")
        self.merchandise_2=models.Merchandise.objects.create(user=self.user_1,
                                                            category='Clothes',
                                                            condition='good',
                                                            description='sdda',
                                                            price=4000,
                                                            title="t-shirt")
        self.merchandise_3=models.Merchandise.objects.create(user=self.user_2,
                                                            category='Clothes',
                                                            condition='good',
                                                            description='sdda',
                                                            price=4000,
                                                            title="jeans")
        self.merchandise_4=models.Merchandise.objects.create(user=self.user_2,
                                                            category='Electronics',
                                                            condition='good',
                                                            description='sdda',
                                                            price=4000,
                                                            title="Computer")



    def test_searchmerchandise_wrong_get_data(self):
        response=self.client.get(reverse('searchmerchandise'),{'tittle':'jeaaans'})
        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, 400)

class MerchandiseTest(APITestCase):
    def setUp(self):
        self.user_1=User.objects.create_user(email='fdgjfd@mail.ru', password='onetwofive', first_name='A', last_name='K')
        self.merchandise_1=models.Merchandise.objects.create(user=self.user_1,
                                                            category='Clothes',
                                                            condition='good',
                                                            description='sdda',
                                                            price=4000,
                                                            title="dress")
        self.user_1.save()
        self.c=Client()
        login=self.c.login(email='fdgjfd@mail.ru',password='onetwofive')
        self.refresh=RefreshToken.for_user(self.user_1)
    #     client=APIClient()
    #     print(self.client.__dict__)
    def test_merchandise_get(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response=self.client.get(reverse('merchandisepk',args=[1])) #after authorization we can get merchandise
        response_data=response.data
        serializer_data=MerchandiseSerializer(self.merchandise_1).data #when having one object response looks like ordinary dict
        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer_data,response_data)

    def test_merchandise_post(self):     #comparing to queryset get 
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        data={'category' : 'Clothes',
             'condition':'good',
             'description':'gfhbgf',
             'price':5000,
             'title':'top'}
        response=self.client.post(reverse('merchandise'), data)
        response_data=response.data
        posted_merchandise=models.Merchandise.objects.get(title='top')
        serializer_data=MerchandiseSerializer(posted_merchandise).data
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data,serializer_data)

    def test_merchandise_post_2(self):    #comparing to self.client.get response
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        post_response=self.client.post(reverse('merchandise'), {'category' : 'Clothes',
                                                                'condition':'good',
                                                                'description':'gfhbgf',
                                                                'price':5000,
                                                                'title':'top'})
        # merchandise=models.Merchandise.objects.get(title='top')
        # print(merchandise.id)
        get_response=self.client.get(reverse('merchandisepk',args=[2]))
        self.assertEqual(post_response.data, get_response.data)
        self.assertEqual(post_response.status_code, 201)

class UserMerchandiseTest(APITestCase):
    def setUp(self):
        self.user_1=User.objects.create_user(email='fdgjfd@mail.ru', password='onetwofive', first_name='A', last_name='K')
        self.merchandise_1=models.Merchandise.objects.create(user=self.user_1,
                                                            category='Clothes',
                                                            condition='good',
                                                            description='sdda',
                                                            price=4000,
                                                            title="dress")
        self.user_1.save()
        # self.c=Client()
        # login=self.c.login(email='fdgjfd@mail.ru',password='onetwofive')
        self.refresh=RefreshToken.for_user(self.user_1)


    def test_mymerchandise_patch(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response=self.client.patch(reverse('mymerchandisepk', args=[1]), {'condition':'excellent'})
        response_data=response.data
        patch_merchandise=models.Merchandise.objects.get(title="dress")
        serializer=MerchandiseSerializer(patch_merchandise)
        serializer_data=serializer.data
        self.assertEqual(response_data,serializer_data)


class DeleteCartTest(APITestCase):
    def setUp(self):
        self.user_1=User.objects.create_user(email='fdgjfd@mail.ru', password='onetwofive', first_name='A', last_name='K')
        self.cart_1=models.Cart.objects.create(user=self.user_1)
        #self.user_1.save()
        self.refresh=RefreshToken.for_user(self.user_1)

    def test_Cart_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response=self.client.delete(reverse('deletecart'))
        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, 204)



#https://github.com/philipn/django-rest-framework-filters/blob/master/tests/test_filterset.py
#https://code.djangoproject.com/ticket/25582
#https://github.com/philipn/django-rest-framework-filters/blob/master/tests/test_filtering.py
#https://stackoverflow.com/questions/46001747/django-test-client-post-data
