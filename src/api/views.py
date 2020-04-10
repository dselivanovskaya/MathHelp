from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View

from .serializers import UserSerializer


class ListUsersView(View):

    def get(self, request):
        '''
            List all users or get a specific user based on
            GET parameters 'username' or/and 'email'.
        '''
        users = User.objects.all()
        username = request.GET.get('username', None)
        email = request.GET.get('email', None)

        if username is not None:
            users = users.filter(username=username)

        if email is not None:
            users = users.filter(email=email)

        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
