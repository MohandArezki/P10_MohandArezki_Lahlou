from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from projects.permissions import ContributorPermissions
from projects.paginations import BasePagination
from projects.models import Contributor, Project
from projects.serializers import ContributorSerializer
from projects.filters import ContributorFilter


class ContributorViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing contributors.

    This viewset allows creating, listing, updating, and deleting contributors associated with projects.

    Pagination, filtering, and search are supported.

    """
    pagination_class = BasePagination
    serializer_class = ContributorSerializer
    permission_classes = [ContributorPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ContributorFilter
    search_fields = ['user__username', 'project__title']

    paginator_list_message = "Listing contributors for the project: {}"
    lookup_field = 'id'

    def get_queryset(self):
        """
        Get the queryset of contributors.

        The queryset is filtered based on the project.

        Returns:
            Queryset: The queryset of contributors.

        """
        project_id = self.kwargs.get("project_pk")
        project = get_object_or_404(Project, pk=project_id)
        self.paginator.message = self.paginator_list_message.format(project)
        return Contributor.objects.filter(project_id=project_id).order_by('role')

    def create(self, request, *args, **kwargs):
        """
        Create a new contributor.

        Args:
            request: The HTTP request.
            args: Additional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response.

        """
        project_id = self.kwargs["project_pk"]
        user_id = self.kwargs["pk"]
        data = {
            "project": project_id,
            "role": "CONTRIBUTOR",
            "user": user_id
        }
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            return Response({'message': 'Contributor created.', 'data': data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = f"An {type(e).__name__} occurred while creating a contributor: {str(e)}"
            return Response({"message": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a contributor.

        Args:
            request: The HTTP request.
            args: Additional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response.

        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Contributor deleted."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_message = f"An {type(e).__name__} occurred while deleting a contributor: {str(e)}"
            return Response({"message": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
