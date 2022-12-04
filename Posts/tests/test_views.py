from django.test import TestCase, Client
from django.urls import reverse, resolve
from rest_framework.test import APIClient, APITestCase
from Posts import models
from Posts.serializers import AllCategoriesSerializer, OnePostSerializer, GetCommentsSerializer, CommentSerializer
from collections import OrderedDict
from Users.models import CustomUser as User
from rest_framework_simplejwt.tokens import RefreshToken

class AllCategoriesTest(APITestCase):

    def setUp(self):
        self.category_1=models.Categories.objects.create(name='Furniture', description='for home')
        self.category_2=models.Categories.objects.create(name='Elecrtonics', description='every kind')
        self.category_3=models.Categories.objects.create(name='Clothes', description='men and women')

    def test_allcategories_get(self):
        response=self.client.get(reverse('allcategories'))
        response_data=response.data
        serializer_data=[OrderedDict(AllCategoriesSerializer(self.category_1).data),
        OrderedDict(AllCategoriesSerializer(self.category_2).data),
        OrderedDict(AllCategoriesSerializer(self.category_3).data)]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer_data,response_data)

class PostTest(APITestCase):

    def setUp(self):
        self.user_1=User.objects.create_user(email='fdgjfd@mail.ru', password='onetwofive', first_name='A', last_name='K')
        self.user_1.save()
        self.refresh=RefreshToken.for_user(self.user_1)
        self.post=models.Post.objects.create(user=self.user_1, title='aa', content='ghf')

    def test_post_get(self):
        response=self.client.get(reverse('getpost', args=[1]))
        response_data=response.data
        serializer_data=OnePostSerializer(self.post).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer_data,response_data)

    def test_post_add(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response=self.client.post(reverse('addpost'), {'title':'accummulator', 'content':'good'})
        response_data=response.data
        added_post=models.Post.objects.get(title='accummulator')
        serializer_data=OnePostSerializer(added_post).data
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data,serializer_data)

    def test_post_patch(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response=self.client.patch(reverse('editpost', args=[1]), {'content':'excellent'})
        response_data=response.data
        patch_post=models.Post.objects.get(title='aa')
        serializer_data=OnePostSerializer(patch_post).data
        self.assertEqual(response_data,serializer_data)
        self.assertEqual(response.status_code, 201)

    def test_post_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response=self.client.delete(reverse('deletepost', args=[1]))
        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, 204)


class AllCommentsTest(APITestCase):
    def setUp(self):
        self.user_2=User.objects.create_user(email='fd@mail.ru', password='onetwo', first_name='D', last_name='K')
        self.post=models.Post.objects.create(user=self.user_2, title='aa', content='ghf')
        self.comment_1=models.Comments.objects.create(content='dfs', post=self.post)
        self.comment_2=models.Comments.objects.create(content='ewe', post=self.post)
        self.comment_3=models.Comments.objects.create(content='fds', post=self.post)

    def test_allcomments_get(self):
        response=self.client.get(reverse('allcomments'))
        response_data=response.data
        serializer_data=[OrderedDict(GetCommentsSerializer(self.comment_1).data),
        OrderedDict(GetCommentsSerializer(self.comment_2).data),
        OrderedDict(GetCommentsSerializer(self.comment_3).data)]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer_data,response_data)

class CommentsTest(APITestCase):

    def setUp(self):
        self.user_1=User.objects.create_user(email='fdgjfd@mail.ru', password='onetwofive', first_name='A', last_name='K')
        self.user_2=User.objects.create_user(email='fd@mail.ru', password='onetwo', first_name='D', last_name='K')
        self.user_3=User.objects.create_user(email='hgfd@mail.ru', password='onetwothree', first_name='B', last_name='K')
        self.user_1.save()
        self.user_2.save()
        self.user_3.save()
        self.refresh=RefreshToken.for_user(self.user_1)
        self.refresh_2=RefreshToken.for_user(self.user_2)
        self.refresh_3=RefreshToken.for_user(self.user_3)
        self.post=models.Post.objects.create(user=self.user_2, title='aa', content='ghf') #chem kara naxord classic vercnem?
        self.comment=models.Comments.objects.create(user=self.user_1, content='dfs', post=self.post)


    def test_comment_add(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response=self.client.post(reverse('addcomment'), {'content':'good', "post":"1"})
        response_data=response.data
        added_comment=models.Comments.objects.get(content='good')
        serializer_data=CommentSerializer(added_comment).data
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data,serializer_data)

    def test_comment_patch(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response=self.client.patch(reverse('editcomment', args=[1]), {'content':'ok'})
        response_data=response.data
        patch_comment=models.Comments.objects.get(content='ok')
        serializer_data=CommentSerializer(patch_comment).data
        self.assertEqual(response_data, serializer_data)
        self.assertEqual(response.status_code, 201)

    def test_comment_delete_by_comment_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response=self.client.delete(reverse('deletecomment', args=[1]))
        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, 204)

    def test_comment_delete_by_post_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh_2.access_token}')
        response=self.client.delete(reverse('deletecomment', args=[1]))
        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, 204)

    def test_comment_delete_by_third_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh_3.access_token}')
        response=self.client.delete(reverse('deletecomment', args=[1]))
        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, 401)
