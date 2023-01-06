from Posts.models import Comments
from Users.models import CustomUser as User
from firebase_admin.messaging import Message, Notification
from django.db.models.signals import post_save
from django.dispatch import receiver
from google.oauth2 import service_account
from .models import WelcomeNotification, CommentNotification



@receiver(post_save, sender=User) #works only when the user is just created
def create_welcome_message(instance, created, **kwargs):
    if not created:
        WelcomeNotification.objects.create(user=instance, # or kwargs.get('instance'), if we dont have instance initially in f()
                                    title='Welcome to our site!',
                                    msg='Thanks for signing up!')

#
@receiver(post_save, sender=Comments)
def post_save_comment(instance, created, **kwargs): #instance is the comment
    if created:
        CommentNotification.objects.create(comment_user=instance.user,
                                        post_user=instance.post.user,
                                        msg=f'{instance.user} commented your post',
                                        comment=instance)
