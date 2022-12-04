from Posts.models import Comments
from Users.models import CustomUser as User
from firebase_admin.messaging import Message, Notification
from django.db.models.signals import post_save
from django.dispatch import receiver
from fcm_django.models import FCMDevice
from google.oauth2 import service_account
from .models import WelcomeNotification, CommentNotification


    # if created:
    #     GCMDevice.objects.create(registration_id="token", cloud_message_type="FCM", user=user)

@receiver(post_save, sender=User) #works only when the user is just created
def create_welcome_message(instance, created, **kwargs):
    if not created:
    #if kwargs.get('created', False): #CREATED-??? DEFAULT VALUE?
        WelcomeNotification.objects.create(user=instance, # or kwargs.get('instance'), if we dont have instance initially in f()
                                    title='Welcome to our site!',
                                    msg='Thanks for signing up!')

#
@receiver(post_save, sender=Comments) #IDK if it works?  6 errors here
def post_save_comment(instance, created, **kwargs): #instance is the comment
    if created:
        notification=CommentNotification.objects.create(comment_user=instance.user,
                                        post_user=instance.post.user,
                                        msg=f'{instance.user} commented your post',
                                        comment=instance)
        # device = FCMDevice.objects.get(user=instance.post.user.id) #instance.post.user.id=1
        # device.send_message(Message(notification=Notification(title="Comment",body=notification.msg)))
        # print('I sent the Notification')
