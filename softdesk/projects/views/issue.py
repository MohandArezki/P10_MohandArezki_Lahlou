from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from projects.paginations import BasePagination
from projects.models import Project, Issue
from projects.serializers import IssueSerializer
from projects.permissions import IssuePermissions
from projects.filters import IssueFilter


class IssueViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing issues.

    This viewset allows creating, listing, updating, and deleting issues associated with projects.

    Pagination, filtering, and search are supported.

    """
    pagination_class = BasePagination
    serializer_class = IssueSerializer
    paginator_list_message = "Listing issues included in the {} project"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = IssueFilter
    search_fields = ['tag', 'status', 'priority', 'title',
                     'project__title', 'author__username', 'assigned__username']
    permission_classes = [IssuePermissions]

    def get_queryset(self):
        """
        Get the queryset of issues.

        The queryset is filtered based on the project.

        Returns:
            Queryset: The queryset of issues.

        """
        project_id = self.kwargs.get("project_pk")
        project = get_object_or_404(Project, pk=project_id)
        self.paginator.message = self.paginator_list_message.format(project)
        return Issue.objects.filter(project_id=project_id).order_by('project')

    def create(self, request, *args, **kwargs):
        """
        Create a new issue.

        Args:
            request: The HTTP request.
            args: Additional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response.

        """
        project_id = self.kwargs.get("project_pk")
        data = request.data
        data["project"] = project_id
        data["author"] = self.request.user.id
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid()
            serializer.save()
            data = serializer.data
            return Response({'message': 'Issue created.', 'data': data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = f"An {type(e).__name__} occurred while creating the project: {str(e)}"
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)
