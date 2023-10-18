from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status

from projects.models import Project
from projects.serializers import ProjectSerializer
from projects.permissions import ProjectPermissions
from projects.paginations import BasePagination
from projects.filters import ProjectFilter


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing projects.

    This viewset allows creating, listing, updating, and deleting projects.

    Pagination, filtering, and search are supported.

    """
    pagination_class = BasePagination
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProjectFilter
    search_fields = ['title', 'type']
    paginator_list_message = "Listing projects that include {} as either the Author or Contributor."

    def get_queryset(self):
        """
        Get the queryset of projects.

        The queryset is filtered based on the user.

        Returns:
            Queryset: The queryset of projects.

        """
        user = self.request.user
        self.paginator.message = self.paginator_list_message.format(user)
        return Project.objects.filter(contributed_project__user=user).order_by('-id')

    def create(self, request, *args, **kwargs):
        """
        Create a new project.

        Args:
            request: The HTTP request.
            args: Additional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response.

        """
        data = request.data
        data['user_id'] = request.user.id
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            return Response({'message': 'Project created.', 'data': data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = f"An {type(e).__name__} occurred while creating the project: {str(e)}"
            return Response({"message": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
