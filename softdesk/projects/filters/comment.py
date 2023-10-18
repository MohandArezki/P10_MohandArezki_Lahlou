import django_filters
from projects.models import Comment


class CommentFilter(django_filters.FilterSet):
    """
    A filter class for Comment model.

    This class defines filters for the Comment model, allowing you to filter
    comments based on various fields such as ID, description, issue title,
    and author.

    Attributes:
        unique_id (CharFilter): Filter for the unique_id field using 'icontains'.
        description (CharFilter): Filter for the description field using 'icontains'.
        issue (CharFilter): Filter for the issue's title field using 'icontains'.
        author (CharFilter): Filter for the author's username field using 'icontains'.

    Meta:
        model (Comment): The model to filter.
        fields (List): List of fields to create filters for.
    """
    unique_id = django_filters.CharFilter(lookup_expr='icontains', label='ID')
    description = django_filters.CharFilter(
        lookup_expr='icontains', label='Description')
    issue = django_filters.CharFilter(
        field_name='issue__title', lookup_expr='icontains', label='Issue Title')
    author = django_filters.CharFilter(
        field_name='author__username', lookup_expr='icontains', label='Author')

    class Meta:
        model = Comment
        fields = ['unique_id', 'description', 'issue', 'author']
