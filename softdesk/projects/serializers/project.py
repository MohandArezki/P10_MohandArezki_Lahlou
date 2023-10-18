from rest_framework import serializers
from projects.models import Project, Contributor
from projects.serializers.issue import IssueSerializer
from projects.serializers.contributor import ContributorSerializer


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for listing projects.

    Fields:
    - id: The unique identifier for the project.
    - title: The title of the project.
    - description: The description of the project.
    - contributors: Serialized contributors associated with the project (read-only, many).
    - issues: Serialized issues associated with the project (read-only, many).
    - user_id: The user ID associated with the project (write-only).

    """
    issues = IssueSerializer(source='project_issues',
                             read_only=True, many=True)
    contributors = ContributorSerializer(
        source='contributed_project', read_only=True, many=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Project
        fields = ['id', 'type', 'title', 'description',
                  'created_time', 'contributors', 'issues', 'user_id']

    def create(self, validated_data):
        """
        Create and return a new Project instance and its associated contributor as "author".
        """
        user_id = validated_data.pop("user_id")
        project = Project.objects.create(**validated_data)
        contributor_data = {"role": "AUTHOR",
                            "project": project, "user_id": user_id}
        Contributor.objects.create(**contributor_data)
        return project
