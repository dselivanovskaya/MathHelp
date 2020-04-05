from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


@receiver(user_logged_in, sender=User)
def increment_login_count(user, **kwargs):
    ''' Every time user logs in, increment his profile login_count. '''
    user.profile.login_count += 1
    user.profile.save()
