from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models


class Issue(models.Model):
    """
    A model representing issues in a project.

    This model stores information about issues, including their tags, status, priority,
    title, description, associated project, author, assigned user, and creation time.

    Attributes:
        tag (CharField): The tag of the issue, such as 'Bug', 'Task', or 'Feature'.
        status (CharField): The status of the issue, such as 'ToDo', 'In Progress', or 'Finished'.
        priority (CharField): The priority of the issue, such as 'Low', 'Medium', or 'High'.
        title (CharField): The title of the issue.
        description (TextField): The description of the issue.
        project (ForeignKey): The project to which the issue is associated.
        author (ForeignKey): The author of the issue, related to the User model.
        assigned (ForeignKey): The user assigned to the issue, related to the User model.
        created_time (DateTimeField): The timestamp when the issue was created.

    Methods:
        is_author(self, user): Checks if the provided user is the author of the issue.
        is_contributor(self, user): Checks if the provided user is a contributor to the project.
    """
    class IssueTag(models.TextChoices):
        BUG = "BUG", _("Bug")
        TASK = "TASK", _("Task")
        FEATURE = "FEATURE", _("Feature")

    class IssueStatus(models.TextChoices):
        TODO = "TODO", _("ToDo")
        INPROGRESS = "INPROGRESS", _("In Progress")
        FINISHED = "FINISHED", _("Finished")

    class IssuePriority(models.TextChoices):
        LOW = "LOW", _("Low")
        MEDIUM = "MEDIUM", _("Medium")
        HIGH = "HIGH", _("High")

    tag = models.CharField(max_length=10, choices=IssueTag.choices, verbose_name=_(
        "Issue Tag"), blank=False, null=False)
    status = models.CharField(max_length=11, choices=IssueStatus.choices,
                              default=IssueStatus.TODO, verbose_name=_("Issue Status"), blank=False, null=False)
    priority = models.CharField(max_length=10, choices=IssuePriority.choices, verbose_name=_(
        "Issue Priority"), blank=False, null=False)
    title = models.CharField(max_length=50, verbose_name=_(
        "Title"), blank=False, null=False)
    description = models.TextField(
        max_length=500, verbose_name=_("Description"))
    project = models.ForeignKey("projects.Project", verbose_name=_(
        "Project"), on_delete=models.CASCADE, related_name="project_issues")
    author = models.ForeignKey("users.User", verbose_name=_(
        "Author"), related_name="authored_issues", null=True, on_delete=models.CASCADE)
    assigned = models.ForeignKey("users.User", verbose_name=_(
        "Assigned"), related_name="assigned_issues", null=True, on_delete=models.CASCADE)
    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created Time"))

    def is_author(self, user):
        return self.author == user

    def is_contributor(self, user):
        return self.project.is_contributor(user)

    def __str__(self):
        return f"(ID:{self.id} - {self.title})"

    def clean(self):
        if not self.project.is_contributor(self.assigned):
            raise ValidationError(_(" 'Assigned' must be a contributor in the project."))
        if not self.project.is_contributor(self.author):
            raise ValidationError(_(" 'Author' must be a contributor in the project."))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
