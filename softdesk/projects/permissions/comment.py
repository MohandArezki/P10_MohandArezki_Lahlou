from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from projects.models import Project, Issue, Comment


class CommentPermissions(BasePermission):
    """
    Custom permissions for comments in the API.

    This class defines custom permissions for comments, including access control
    based on the user's authentication status and their relationship to the project,
    issue, and comment.

    Methods:
        has_permission(self, request, view): Checks if the user has permission to perform the requested action.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        project = get_object_or_404(Project, id=view.kwargs['project_pk'])
        issue = None

        if 'issue_pk' in view.kwargs:
            issue = get_object_or_404(Issue, id=view.kwargs['issue_pk'])

        if request.method in ['GET', 'POST']:
            if issue:
                return project.is_contributor(request.user) and issue.is_contributor(request.user)
            return project.is_contributor(request.user)

        if 'pk' in view.kwargs:
            comment = get_object_or_404(Comment, unique_id=view.kwargs['pk'])
            return comment.is_author(request.user)

        return False
