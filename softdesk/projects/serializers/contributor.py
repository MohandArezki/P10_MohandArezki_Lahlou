from rest_framework import serializers
from projects.models import Contributor
from users.serializers import UserListSerializer


class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contributor model.

    Fields:
    - id: The unique identifier for the contributor.
    - role: The role of the contributor in the project.
    - user: The user associated with the contributor.
    - user_details: Serialized user details (read-only).
    - project: The project to which the contributor is associated (write-only).

    """
    user_details = UserListSerializer(source='user', read_only=True)

    class Meta:
        model = Contributor
        fields = ['id', 'role', 'user', 'user_details', 'project']

        extra_kwargs = {
            'project': {'write_only': True},
            'user': {'write_only': True}
        }
