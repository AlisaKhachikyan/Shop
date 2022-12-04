from django.urls import path
from .import views


urlpatterns = [
        path('welcomenotification/<int:pk>', views.WelcomeNotificationView.as_view(), name='welcomenotification'),
        path('commentnotification/<int:pk>', views.CommentNotificationView.as_view(), name='commentnotification'),
        path('my-commentnotifications/', views.MyCommentNotificationList.as_view(), name='mycommentnotifications'),
]
