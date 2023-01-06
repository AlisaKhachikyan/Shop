from django.test import TestCase
from django.urls import reverse, resolve
from Notification import views


class TestUrls(TestCase):
    def test_welcomenotification_url(self):
        url=reverse('welcomenotification', args=[1])
        self.assertEquals(resolve(url).func.view_class, views.WelcomeNotificationView)

    def test_commentnotification_url(self):
        url=reverse('commentnotification', args=[1])
        self.assertEquals(resolve(url).func.view_class, views.CommentNotificationView)

    def test_mycommentnotifications_url(self):
        url=reverse('mycommentnotifications')
        self.assertEquals(resolve(url).func.view_class, views.MyCommentNotificationList)
