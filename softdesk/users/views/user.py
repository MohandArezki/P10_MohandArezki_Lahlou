from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.generics import get_object_or_404

from users.serializers import LoginSerializer, LogoutSerializer, UserSerializer
from users.models import User


class UserViewSet(APIView):
    """
    A view set for managing user profiles.

    - GET: Retrieve the authenticated user's profile.
    - PATCH: Update the authenticated user's profile.
    - DELETE: Delete the authenticated user's profile.
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_connected_user(self):
        """
        Get the currently authenticated user.
        """
        user = self.request.user
        return get_object_or_404(User, pk=user.pk)

    def get(self, request, *args, **kwargs):
        """
        Retrieve the profile of the authenticated user.
        """
        user = self.get_connected_user()
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """
        Update the profile of the authenticated user.
        """
        user = self.get_connected_user()
        serializer = self.serializer_class(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response({'message': 'Profile update successfully', 'data': data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Delete the profile of the authenticated user.
        """
        user = self.get_connected_user()
        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class RegisterAPIView(APIView):
    """
    A view for user registration.

    - POST: Register a new user.
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """
        Register a new user.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response({'message': 'User registration successful', 'data': data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """
    A view for user login.

    - POST: Authenticate and log in a user.
    """
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Authenticate and log in a user.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            return Response({'message': 'Login successfully', 'data': data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(generics.GenericAPIView):
    """
    A view for user logout.

    - POST: Log out the authenticated user.
    """
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """
        Log out the authenticated user.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Logout successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
