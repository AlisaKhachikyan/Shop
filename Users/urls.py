from django.urls import path
from .import views


urlpatterns = [
        path('all_users', views.AllUsers.as_view()),
        path('user', views.User.as_view()),
        path('register', views.RegisterView.as_view()),
]
