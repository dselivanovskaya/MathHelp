from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


@receiver(user_logged_in)
def increment_login_count(request, user, **kwargs):
    ''' Every time user logs in, increment his profile login_count. '''
    user.profile.login_count += 1
    user.profile.save()


@receiver(user_logged_in)
def initialize_session_entries(request, user, **kwargs):
    request.session['read_tickets'] = []
    request.session['taken_quizzes'] = {}
