from django.urls import path, include
from rest_framework.routers import DefaultRouter
from projects.views import ContributorViewSet, ProjectViewSet, IssueViewSet, CommentViewSet

# Create a router for projects
project_router = DefaultRouter()
project_router.register(r'projects', ProjectViewSet, basename='project')

# Create separate views for contributors, issues, and comments within projects
urlpatterns = [
    # Include the URLs generated by the DefaultRouter for projects
    path('', include(project_router.urls)),

    # Contributors URLs
    path('projects/<int:project_pk>/contributors/', ContributorViewSet.as_view({'get': 'list'}),
         name='project-contributors'),
    path('projects/<int:project_pk>/contributors/<int:pk>/', ContributorViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}), name='project-contributor-detail'),

    # Issues URLs
    path('projects/<int:project_pk>/issues/', IssueViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='project-issues'),
    path('projects/<int:project_pk>/issues/<int:pk>/', IssueViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='project-issue-detail'),

    # Comments URLs
    path('projects/<int:project_pk>/issues/<int:issue_pk>/comments/', CommentViewSet.as_view(
        {'post': 'create', 'get': 'list'}), name='comment-list-create'),
    path('projects/<int:project_pk>/issues/<int:issue_pk>/comments/<uuid:pk>/', CommentViewSet.as_view(
        {'put': 'update', 'patch': 'partial_update', 'get': 'retrieve', 'delete': 'destroy'}), name='comment-get-update-destroy'),

    # Comments List URL
    path('projects/<int:project_pk>/comments/', CommentViewSet.as_view({'get': 'list'}),
         name='comments-list'),
]