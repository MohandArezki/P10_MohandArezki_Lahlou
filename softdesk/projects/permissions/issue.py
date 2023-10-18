from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.generics import get_object_or_404
from projects.models import Project, Issue


class IssuePermissions(BasePermission):
    """
    Custom permissions for issues in the API.

    This class defines custom permissions for issues, including access control
    based on the user's authentication status, their role in the project, and the HTTP method.

    Methods:
        has_permission(self, request, view): Checks if the user has permission to perform the requested action.
    """

    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['project_pk'])

        if request.user and request.user.is_authenticated:

            if request.method in SAFE_METHODS:
                return project.is_contributor(request.user)

            if request.method == 'POST':
                return project.is_author(request.user)

            issue = get_object_or_404(Issue, id=view.kwargs['pk'])
            return issue.is_author(request.user)
