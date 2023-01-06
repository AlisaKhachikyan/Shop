from django.test import TestCase
from django.urls import reverse, resolve
from Users import views


class TestUrls(TestCase):
    def test_allusers_url(self):
        url=reverse('allusers')
        self.assertEquals(resolve(url).func.view_class, views.AllUsers)

    def test_myuser_url(self):
        url=reverse('myuser')
        self.assertEquals(resolve(url).func.view_class, views.MyUser)

    def test_user_url(self):
        url=reverse('oneuser', args=[1])
        self.assertEquals(resolve(url).func.view_class, views.User)

    def test_register_url(self):
        url=reverse('register')
        self.assertEquals(resolve(url).func.view_class, views.RegisterView)

    def test_search_url(self):
        url=reverse('searchuser')
        self.assertEquals(resolve(url).func.view_class, views.SearchUser)
