from django.contrib.auth.models import User
from django.views import View
from django.http import JsonResponse

from .serializers import UserSerializer


class ListUsersView(View):

    def get(self, request):
        ''' Return a list of all users. '''

        users = User.objects.all()
        username = request.GET.get('username', None)
        email = request.GET.get('email', None)

        if username is not None:
            users = users.filter(username=username)

        if email is not None:
            users = users.filter(email=email)

        serializer = UserSerializer(users, many=True)

        return JsonResponse(serializer.data, safe=False)
