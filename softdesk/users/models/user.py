from datetime import date
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    """
    Custom user model with additional fields.

    Attributes:
    - date_of_birth: The user's date of birth.
    - can_be_contacted: Boolean indicating if the user can be contacted.
    - can_share_data: Boolean indicating if the user can share data.

    Fields:
    - username: The unique username for the user.
    - email: The user's email address (required).
    - date_of_birth: The user's date of birth (required).

    Methods:
    - tokens(): Generate JWT tokens for the user.
    - clean(): Validate the user's age to be older than 15 years.
    - save(): Override the save method to perform validation before saving.
    - __str__(): Return a string representation of the user.

    """

    date_of_birth = models.DateField(verbose_name='Date of birth')
    can_be_contacted = models.BooleanField(
        verbose_name='User can be Contacted', default=False)
    can_share_data = models.BooleanField(
        verbose_name='User can share data', default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'date_of_birth']

    def tokens(self):
        """
        Generate JWT tokens for the user.

        Returns:
        A dictionary containing 'refresh' and 'access' tokens.
        """
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def clean(self):
        """
        Validate the user's age to be older than 15 years.

        Raises:
        ValidationError: If the user is younger than 15 years.
        """
        dob = self.date_of_birth
        today = date.today()
        age = today.year - dob.year - \
            ((today.month, today.day) < (dob.month, dob.day))

        if age <= 15:
            raise ValidationError('User must be older than 15 years.')

    def save(self, *args, **kwargs):
        """
        Override the save method to perform validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return a string representation of the user.

        Returns:
        A string in the format "(ID: {user_id} - {username})".
        """
        return f"(ID:{self.id} - {self.username})"
