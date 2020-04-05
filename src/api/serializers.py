from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    gender = serializers.IntegerField(source='profile.gender')
    login_count = serializers.IntegerField(source='profile.login_count')

    class Meta:
        model = User
        fields = ('username', 'email', 'gender', 'login_count')
