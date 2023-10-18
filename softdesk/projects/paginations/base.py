from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BasePagination(PageNumberPagination):
    """
    Base pagination class for consistent response structure.

    Attributes:
    - page_size (int): The number of items to include per page.
    - message (str): The default message for the paginated response.

    Methods:
    - get_paginated_response(data): Generate a paginated response with a custom message.

    """
    page_size = 10
    message = 'list'

    def get_paginated_response(self, data):
        """
        Generate a paginated response with a custom message.

        Args:
        - data (list): The paginated data.

        Returns:
        - Response: Paginated response object containing the message, count, next, previous, and results.

        """
        return Response({
            "message": self.message,
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data
        })
