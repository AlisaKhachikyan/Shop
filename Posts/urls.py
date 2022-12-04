from django.urls import path
from .import views


urlpatterns = [
        path('all_categories', views.AllCategories.as_view(), name='allcategories'),
        path('post_get/<int:pk>', views.GetPost.as_view(), name='getpost'),
        path('post_add/', views.AddPost.as_view(), name= 'addpost' ),
        path('post_edit/<int:pk>', views.EditPost.as_view(), name= "editpost"),
        path('post_delete/<int:pk>', views.DeletePost.as_view(), name= "deletepost"),
        path('all_comments/', views.AllComments.as_view(), name='allcomments'),
        path('comment_add/', views.AddComment.as_view(), name= 'addcomment' ),
        path('comment_edit/<int:pk>', views.EditComment.as_view(), name= "editcomment"),
        path('comment_delete/<int:pk>', views.DeleteComment.as_view(), name= "deletecomment"),
]
#http_method_names=['POST']
