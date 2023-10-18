from rest_framework import serializers
from projects.models import Issue
from users.serializers import UserListSerializer


class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer for the Issue model.

    Fields:
    - id: The unique identifier for the issue.
    - tag: The tag/category of the issue.
    - status: The status of the issue.
    - priority: The priority of the issue.
    - title: The title of the issue.
    - description: The description of the issue.
    - project: The project to which the issue is associated (write-only).
    - author: The author of the issue.
    - assigned: The user assigned to the issue.
    - author_details: Serialized author details (read-only).
    - assigned_details: Serialized details of the assigned user (read-only).

    """
    author_details = UserListSerializer(source='author', read_only=True)
    assigned_details = UserListSerializer(source='assigned', read_only=True)

    class Meta:
        model = Issue
        fields = ['id', 'tag', 'status', 'priority', 'title', 'description',
                  'project', 'author', 'assigned', 'author_details', 'assigned_details'
                  ]

        extra_kwargs = {
            'project': {'write_only': True},
            'user': {'write_only': True}
        }
