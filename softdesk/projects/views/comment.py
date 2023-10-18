from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from projects.paginations import BasePagination
from projects.models import Project, Comment, Issue
from projects.serializers import CommentSerializer
from projects.permissions import CommentPermissions
from projects.filters import CommentFilter


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing comments.

    This viewset allows creating, listing, updating, and deleting comments associated with projects and issues.

    Pagination, filtering, and search are supported.

    """
    pagination_class = BasePagination
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CommentFilter
    search_fields = ['unique_id', 'description']
    paginator_list_message = "Listing comments included in the {} project"
    permission_classes = [CommentPermissions]

    def get_queryset(self):
        """
        Get the queryset of comments.

        The queryset is filtered based on the project and issue, if provided.

        Returns:
            Queryset: The queryset of comments.

        """
        project_id = self.kwargs.get("project_pk")
        issue_id = self.kwargs.get("issue_pk")

        project = get_object_or_404(Project, pk=project_id)

        queryset = Comment.objects.filter(
            issue__project=project).order_by('author')
        self.paginator.message = self.paginator_list_message.format(project)

        if issue_id is not None:
            issue = get_object_or_404(Issue, pk=issue_id)
            self.paginator.message = "Listing comments included in the {} issue of {} project".format(
                issue, project)
            queryset = queryset.filter(issue=issue)

        return queryset

    def create(self, request, *args, **kwargs):
        """
        Create a new comment.

        Args:
            request: The HTTP request.
            args: Additional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response.

        """
        data = request.data
        data["author"] = self.request.user.id
        data['issue'] = self.kwargs["issue_pk"]
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid()
            serializer.save()
            data = serializer.data
            return Response({'message': 'Comment created.', 'data': data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = f"An {type(e).__name__} occurred while creating a comment: {str(e)}"
            return Response({"message": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
