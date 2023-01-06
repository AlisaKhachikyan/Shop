from django.urls import path
from .import views


urlpatterns = [
        path('all_users', views.AllUsers.as_view(), name='allusers'),
        path('myuser', views.MyUser.as_view(), name='myuser'),
        path('user/<int:pk>', views.User.as_view(), name='oneuser'),
        path('register', views.RegisterView.as_view(), name='register'),
        path('search', views.SearchUser.as_view(), name='searchuser'),
]
