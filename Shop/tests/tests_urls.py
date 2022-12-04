from django.test import TestCase, Client
from django.urls import reverse, resolve
from Shop import views
# Create your tests here.

class TestUrls(TestCase):
    def test_allmerchandises_url(self):
        url=reverse('allmerchandises') #reverse принимает ввод имени URL-адреса и дает фактический URL-адрес, который является обратным тому, чтобы сначала иметь URL-адрес, а затем дать ему имя.
        self.assertEquals(resolve(url).func.view_class, views.AllMerchandises)
    def test_merchandise(self):
        url=reverse('merchandisepk',args=[1])
        self.assertEquals(resolve(url).func.view_class, views.Merchandise)
    def test_mymerchandise(self):
        url=reverse('mymerchandisepk', args=[1])
        self.assertEquals(resolve(url).func.view_class, views.UserMerchandise)
    def test_addcartitem(self):
        url=reverse('addcartitem')
        self.assertEquals(resolve(url).func.view_class, views.AddCartItem)
    def test_getcart(self):
        url=reverse('getcartpk', args=[1])
        self.assertEquals(resolve(url).func.view_class, views.GetCart)
    def test_deletecart(self):
        url=reverse('deletecart')
        self.assertEquals(resolve(url).func.view_class, views.DeleteCart) #204 or 405
    def test_searchmerchandise(self):
        url=reverse('searchmerchandise')
        self.assertEquals(resolve(url).func.view_class, views.SearchMerchandise)
