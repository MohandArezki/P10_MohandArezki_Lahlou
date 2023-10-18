import django_filters
from projects.models import Issue


class IssueFilter(django_filters.FilterSet):
    """
    A filter class for Issue model.

    This class defines filters for the Issue model, allowing you to filter
    issues based on various fields such as tags, status, priority, title,
    associated project's title, author's username, and assigned user's username.

    Attributes:
        tag (CharFilter): Filter for the tag field using 'icontains'.
        status (CharFilter): Filter for the status field using 'icontains'.
        priority (CharFilter): Filter for the priority field using 'icontains'.
        title (CharFilter): Filter for the title field using 'icontains'.
        project (CharFilter): Filter for the project's title using 'icontains'.
        author (CharFilter): Filter for the author's username using 'icontains'.
        assigned (CharFilter): Filter for the assigned user's username using 'icontains'.

    Meta:
        model (Issue): The model to filter.
        fields (List): List of fields to create filters for.
    """
    tag = django_filters.CharFilter(lookup_expr='icontains', label='Tag')
    status = django_filters.CharFilter(lookup_expr='icontains', label='Status')
    priority = django_filters.CharFilter(
        lookup_expr='icontains', label='Priority')
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title')
    project = django_filters.CharFilter(
        field_name='project__title', lookup_expr='icontains', label='Project')
    author = django_filters.CharFilter(
        field_name='author__username', lookup_expr='icontains', label='Author')
    assigned = django_filters.CharFilter(
        field_name='assigned__username', lookup_expr='icontains', label='Assigned')

    class Meta:
        model = Issue
        fields = ['tag', 'status', 'priority',
                  'title', 'project', 'author', 'assigned']
