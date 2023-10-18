from django.urls import path
from users.views import UserViewSet, LoginAPIView, LogoutAPIView, RegisterAPIView

urlpatterns = [
    # Endpoint for viewing the user's profile
    path('user/profile/', UserViewSet.as_view(), name='user-profile'),

    # Endpoint for updating the user's profile
    path('user/profile/update/', UserViewSet.as_view(),
         name='update-user-profile'),

    # Endpoint for deleting the user's account
    path('user/profile/delete/', UserViewSet.as_view(),
         name='delete-user-profile'),

    # Endpoint for user registration
    path('register/', RegisterAPIView.as_view(), name='register'),

    # Endpoint for user login
    path('login/', LoginAPIView.as_view(), name='login'),

    # Endpoint for user logout
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]
