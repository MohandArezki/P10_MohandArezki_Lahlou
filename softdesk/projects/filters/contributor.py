import django_filters
from projects.models import Contributor


class ContributorFilter(django_filters.FilterSet):
    """
    A filter class for Contributor model.

    This class defines filters for the Contributor model, allowing you to filter
    contributors based on the associated user's username and project's title.

    Attributes:
        user (CharFilter): Filter for the user's username using 'icontains'.
        project (CharFilter): Filter for the project's title using 'icontains'.

    Meta:
        model (Contributor): The model to filter.
        fields (List): List of fields to create filters for.
    """
    user = django_filters.CharFilter(
        field_name='user__username', lookup_expr='icontains', label='User')
    project = django_filters.CharFilter(
        field_name='project__title', lookup_expr='icontains', label='Project')

    class Meta:
        model = Contributor
        fields = ['user', 'project']
