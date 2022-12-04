from django.test import TestCase, Client
from django.urls import reverse, resolve
from rest_framework.test import APIClient, APITestCase
from Users.models import CustomUser as User
from rest_framework_simplejwt.tokens import RefreshToken
from Notification.serializers import WelcomeNotificationSerializer, CommentNotificationSerializer
from Notification.models import WelcomeNotification, CommentNotification
from Posts.models import Comments, Post

class WelcomeNotificationTest(APITestCase):

    def setUp(self):
        self.user=User.objects.create_user(email='fdfvgjfd@mail.ru', password='onetwofive', first_name='A', last_name='K')
        self.user.save()
        self.refresh=RefreshToken.for_user(self.user)

    def test_welcomenotification_get(self):
        response=self.client.get(reverse('welcomenotification', args=[1]))
        response_data=response.data
        serializer_data=WelcomeNotificationSerializer(WelcomeNotification.objects.get(id=1)).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer_data,response_data)

    def test_welcomenotification_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}') #???
        response=self.client.delete(reverse('welcomenotification', args=[1]))
        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, 204)

class CommentNotificationTest(APITestCase):

    def setUp(self):
        self.user=User.objects.create_user(email='fdfvgjfd@mail.ru', password='onetwofive', first_name='A', last_name='K')
        self.post=Post.objects.create(title='ds', content='fdfd', user=self.user)
        self.comment=Comments.objects.create(content='nice', post=self.post)
        self.refresh=RefreshToken.for_user(self.user)

    def test_commentnotification_get(self):
        response=self.client.get(reverse('commentnotification', args=[1]))
        response_data=response.data
        serializer_data=CommentNotificationSerializer(CommentNotification.objects.get(id=1)).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer_data,response_data)

    def test_commentnotification_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response=self.client.delete(reverse('commentnotification', args=[1]))
        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, 204)
