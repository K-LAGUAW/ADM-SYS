from rest_framework import generics
from .models import User
from .serializers import UserSerializer

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-creation_date')
    serializer_class = UserSerializer