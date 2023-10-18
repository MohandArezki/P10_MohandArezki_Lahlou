from rest_framework.permissions import BasePermission, SAFE_METHODS


class ProjectPermissions(BasePermission):
    """
    Custom permissions for projects in the API.

    This class defines custom permissions for projects, including access control
    based on the user's authentication status, their role in the project, and the HTTP method.

    Methods:
        has_object_permission(self, request, view, obj): Checks if the user has permission to perform the requested action on a specific project object.
    """

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            user = request.user
            if request.method in SAFE_METHODS:
                return obj.is_contributor(user)
            return obj.is_author(user)
        return False
