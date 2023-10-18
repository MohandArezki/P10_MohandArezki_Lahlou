from django.utils.translation import gettext_lazy as _
from django.db import models


class Project(models.Model):
    """
    A model representing projects of different types.

    This model stores information about projects, including their type (e.g., Back-End, Front-End, iOS, Android),
    title, description, and creation time.

    Attributes:
        type (CharField): The type of the project, chosen from predefined choices.
        title (CharField): The title of the project.
        description (TextField): A description of the project.
        created_time (DateTimeField): The timestamp when the project was created.

    Methods:
        is_author(self, user): Checks if the provided user is the author of the project.
        is_contributor(self, user): Checks if the provided user is a contributor to the project.
    """

    class ProjectType(models.TextChoices):
        BACK_END = "BACK-END", _('Back-End')
        FRONT_END = "FRONT-END", _('Front-End')
        IOS = "IOS", 'iOS'
        ANDROID = "ANDROID", _('Android')

    type = models.CharField(max_length=10, choices=ProjectType.choices, verbose_name=_(
        "Project Type"), blank=False, null=False)
    title = models.CharField(max_length=50, verbose_name=_(
        "Title"), blank=False, null=False)
    description = models.TextField(
        max_length=500, verbose_name=_("Description"))
    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created Time"))

    def is_author(self, user):
        return self.contributed_project.filter(user=user, role='AUTHOR').exists()

    def is_contributor(self, user):
        return self.contributed_project.filter(user=user).exists()

    def __str__(self):
        return f"(ID:{self.id} - {self.title})"
