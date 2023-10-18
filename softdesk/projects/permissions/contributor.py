from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.generics import get_object_or_404
from projects.models import Project


class ContributorPermissions(BasePermission):
    """
    Custom permissions for contributors in the API.

    This class defines custom permissions for contributors, including access control
    based on the user's authentication status and their role in the project.

    Methods:
        has_permission(self, request, view): Checks if the user has permission to perform the requested action.
    """

    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['project_pk'])
        if request.method in SAFE_METHODS:
            return project.is_contributor(request.user)
        return project.is_author(request.user)
