from django.urls import path
from .import views


urlpatterns = [path('all-merchandises', views.AllMerchandises.as_view(), name='allmerchandises'),
               path('merchandise/<int:pk>', views.Merchandise.as_view(), name='merchandisepk'),
               path('merchandise', views.Merchandise.as_view(), name='merchandise'),
               path('my-merchandise', views.UserMerchandise.as_view(), name='mymerchandise'),
               path('my-merchandise/<int:pk>', views.UserMerchandise.as_view(), name='mymerchandisepk'),
               path('add-cart-item', views.AddCartItem.as_view(), name='addcartitem'),
               path('get-cart', views.GetCart.as_view(), name='getcart'),
               path('get-cart/<int:pk>', views.GetCart.as_view(), name='getcartpk'),
               path('delete-cart', views.DeleteCart.as_view(), name='deletecart'),
               path('search-merchandise', views.SearchMerchandise.as_view(), name='searchmerchandise'),
]
