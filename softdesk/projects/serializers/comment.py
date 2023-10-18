from rest_framework import serializers
from projects.models import Comment
from users.serializers import UserListSerializer
from django.urls import reverse


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for listing comments.

    Fields:
    - unique_id: The unique identifier for the comment.
    - description: The description of the comment.
    - author: The author of the comment (read-only).
    - author_details: Details of the author (read-only).
    - issue_url: The URL of the associated issue.

    """
    author_details = UserListSerializer(source='author', read_only=True)
    issue_url = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("unique_id", "description", 'author',
                  'author_details', 'issue', 'issue_url')
        extra_kwargs = {
            'issue': {'write_only': True},
            'author': {'write_only': True}
        }

    def get_issue_url(self, obj):
        request = self.context.get('request')
        project_pk = self.context.get('view').kwargs.get('project_pk')

        # Construct the URL based on the view name and parameters
        url = request.build_absolute_uri(reverse(
            'projects:project-issue-detail', kwargs={'project_pk': project_pk, 'pk': obj.issue.id}))
        return url
