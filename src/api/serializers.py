from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):

    gender = serializers.CharField(max_length=1, source='profile.gender')
    age = serializers.IntegerField(source='profile.age')
    login_count = serializers.IntegerField(source='profile.login_count')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',
                  'gender', 'age', 'login_count')
