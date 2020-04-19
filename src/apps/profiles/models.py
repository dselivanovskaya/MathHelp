from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    MALE, FEMALE = 'M', 'F'
    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MALE)
    age = models.PositiveSmallIntegerField(default=0)

    image = models.ImageField(upload_to='profiles/photos', default='profiles/photos/default-avatar.jpg')
    login_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return (f"Profile(user={self.user}, "
                f"gender={self.gender}, "
                f"age={self.age}, "
                f"login_count={self.login_count})")

    def is_male(self):
        return self.gender == self.MALE

    def is_female(self):
        return self.gender == self.FEMALE
