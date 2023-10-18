from django.contrib import admin

from .models.project import Project
from .models.contributor import Contributor
from .models.issue import Issue
from .models.comment import Comment


class ProjectAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Project model.

    Attributes:
    - list_display: Fields to display in the project list view.
    - display_contributors(obj): Custom method to display contributors in the list view.
    """

    list_display = ['id', 'type', 'title', 'display_contributors']

    def display_contributors(self, obj):
        """
        Display contributors in a user-friendly format in the list view.

        Args:
        - obj: The Project instance.

        Returns:
        - str: A formatted string of contributors.
        """
        contributors = obj.contributed_project.all()
        contributor_names = []

        for contributor in contributors:
            if contributor.role == Contributor.ContributorRole.AUTHOR:
                contributor_names.append(
                    f"{contributor.user.username} ({contributor.get_role_display()})")
            else:
                contributor_names.append(contributor.user.username)

        return ', '.join(contributor_names)

    display_contributors.short_description = 'Contributors'


class ContributorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Contributor model.

    Attributes:
    - list_display: Fields to display in the contributor list view.
    """

    list_display = ['id', 'user', 'role', 'project']


class IssueAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Issue model.

    Attributes:
    - list_display: Fields to display in the issue list view.
    """

    list_display = ['id', 'project', 'tag', 'status', 'priority',
                    'title', 'description', 'author', 'assigned', 'created_time']


class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Comment model.

    Attributes:
    - list_display: Fields to display in the comment list view.
    """

    list_display = ['unique_id', 'description',
                    'issue', 'author', 'created_time']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
