from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models
import uuid


class Comment(models.Model):
    """
    A model representing comments on issues in a project.

    This model stores information about comments, including a unique ID, description,
    the associated issue, the author of the comment, and the creation time.

    Attributes:
        unique_id (UUIDField): A unique identifier for the comment.
        description (TextField): The description of the comment.
        issue (ForeignKey): The associated issue where the comment is made.
        author (ForeignKey): The author of the comment, related to the User model.
        created_time (DateTimeField): The timestamp when the comment was created.

    Methods:
        is_author(self, user): Checks if the provided user is the author of the comment.
        is_contributor(self, user): Checks if the provided user is a contributor on the project.
    """

    unique_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=500, verbose_name=_(
        "Description"), blank=False, null=False)
    issue = models.ForeignKey(
        "projects.Issue", on_delete=models.CASCADE, related_name="commented_issue")
    author = models.ForeignKey("users.User", verbose_name=_(
        "Author"), related_name="authored_comments", null=True, on_delete=models.CASCADE)
    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created Time"))

    def is_author(self, user):
        return self.author == user

    def is_contributor(self, user):
        return self.issue.is_contributor(user)

    def __str__(self):
        return f"Comment {self.unique_id}"

    def clean(self):
        if not self.issue.is_contributor(self.author):
            raise ValidationError(
                _("The author must be a contributor on the project."))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
