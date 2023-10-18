from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models


class Contributor(models.Model):
    """
    A model representing contributors to projects.

    This model stores information about contributors, including their role (author or contributor),
    the associated user, the project they are contributing to, and the creation time.

    Attributes:
        role (CharField): The role of the contributor, either 'Author' or 'Contributor'.
        user (ForeignKey): The user associated with the contributor.
        project (ForeignKey): The project to which the contributor is associated.
        created_time (DateTimeField): The timestamp when the contributor was added to the project.

    Methods:
        is_author(self, user): Checks if the provided user is the author of the project.
        is_contributor(self, user): Checks if the provided user is a contributor to the project.
    """

    class ContributorRole(models.TextChoices):
        AUTHOR = "AUTHOR", _("Author")
        CONTRIBUTOR = "CONTRIBUTOR", _("Contributor")

    role = models.CharField(max_length=11, choices=ContributorRole.choices,
                            default=ContributorRole.CONTRIBUTOR, verbose_name=_("Role"))
    user = models.ForeignKey("users.User", verbose_name=_(
        "Contributor"), related_name="contributor_projects", null=True, on_delete=models.CASCADE)
    project = models.ForeignKey("projects.Project", verbose_name=_(
        "Project"), on_delete=models.CASCADE, related_name="contributed_project")
    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created Time"))

    def is_author(self, user):
        return self.project.is_author(user)

    def is_contributor(self, user):
        return self.project.is_contributor(user)

    def __str__(self):
        return f'{self.user}'

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('user', 'project',)

    def clean(self):
        """
        Ensure that there's only one 'AUTHOR' per project.
        """
        if self.role == Contributor.ContributorRole.AUTHOR:
            existing_author = Contributor.objects.filter(
                project=self.project, role=Contributor.ContributorRole.AUTHOR).exclude(id=self.id).exists()
            if existing_author:
                raise ValidationError(
                    _("A user is already assigned to the project as 'author'."))
