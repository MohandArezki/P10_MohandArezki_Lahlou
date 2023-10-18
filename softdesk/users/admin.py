from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    """
    Admin configuration for the User model.

    Displays the following fields in the admin list view:
    - id
    - username
    - email
    - date_of_birth
    - can_be_contacted
    - can_share_data
    - date_joined

    """
    list_display = ('id', 'username', 'email', 'date_of_birth',
                    'can_be_contacted', 'can_share_data', 'date_joined')


# Register the User model with the custom admin configuration
admin.site.register(User, UserAdmin)
