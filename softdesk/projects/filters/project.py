import django_filters
from projects.models import Project


class ProjectFilter(django_filters.FilterSet):
    """
    A filter class for Project model.

    This class defines filters for the Project model, allowing you to filter
    projects based on fields such as title and type.

    Attributes:
        title (CharFilter): Filter for the project's title using 'icontains'.
        type (CharFilter): Filter for the project's type using 'icontains'.

    Meta:
        model (Project): The model to filter.
        fields (List): List of fields to create filters for.
    """
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title')
    type = django_filters.CharFilter(lookup_expr='icontains', label='Type')

    class Meta:
        model = Project
        fields = ['title', 'type']
