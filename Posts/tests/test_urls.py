from django.test import TestCase
from django.urls import reverse, resolve
from Posts import views
# Create your tests here.

class TestUrls(TestCase):
    def test_allcategories_url(self):
        url=reverse('allcategories')
        self.assertEquals(resolve(url).func.view_class, views.AllCategories)

    def test_post_get_url(self):
        url=reverse('getpost', args=[1])
        self.assertEquals(resolve(url).func.view_class, views.GetPost)

    def test_post_add_url(self):
        url=reverse('addpost')
        self.assertEquals(resolve(url).func.view_class, views.AddPost)

    def test_post_patch_url(self):
        url=reverse('editpost', args=[1])
        self.assertEquals(resolve(url).func.view_class, views.EditPost)

    def test_post_delete_url(self):
        url=reverse('deletepost', args=[1])
        self.assertEquals(resolve(url).func.view_class, views.DeletePost)

    def test_allcomments_url(self):
        url=reverse('allcomments')
        self.assertEquals(resolve(url).func.view_class, views.AllComments)

    def test_addcomment_url(self):
        url=reverse('addcomment')
        self.assertEquals(resolve(url).func.view_class, views.AddComment)

    def test_comment_patch_url(self):
        url=reverse('editcomment', args=[1])
        self.assertEquals(resolve(url).func.view_class, views.EditComment)

    def test_comment_delete_url(self):
        url=reverse('deletecomment', args=[1])
        self.assertEquals(resolve(url).func.view_class, views.DeleteComment)
