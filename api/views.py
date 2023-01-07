from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User, Order
from api.serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer, OrderSerializer

import jwt


class UserView(generics.ListCreateAPIView):
    """
        API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_classes = [UserSerializer, RegisterSerializer]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return RegisterSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        API endpoint that allows user to be viewed or edited.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
        API endpoint that allows user to change password.
    """
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    # lookup_field = 'id'


class OrderView(APIView):
    """
        API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        if request.auth is not None:
            email = request.user
            queryset = Order.objects.filter(user__email=email)
            queryset_with_no_user = Order.objects.filter(user=None)
            serializer = OrderSerializer(queryset, many=True)
            serializer2 = OrderSerializer(queryset_with_no_user, many=True)
            return Response({"this user": serializer.data, "null users": serializer2.data})
        queryset = Order.objects.filter(user=None)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if 'status' in request.data:
            return Response({"error": "Status must be changed from admin panel only!"},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        API endpoint that allows user to be viewed or edited.
    """
    queryset = Order.objects.all()
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer
