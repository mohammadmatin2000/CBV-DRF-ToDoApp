from rest_framework import pagination
from rest_framework.response import Response

# ======================================================================================================================
# CustomPagination: A custom pagination class using Django REST framework's PageNumberPagination
class CustomPagination(pagination.PageNumberPagination):
    """
    This class customizes pagination behavior for API responses.
    """

    page_size = 2  # Defines the number of objects per page (default: 2)

    def get_paginated_response(self, data):
        """
        Customizes the paginated response format.
        """
        return Response({
            'links': {
                'next': self.get_next_link(),  # URL to the next page if available
                'previous': self.get_previous_link()  # URL to the previous page if available
            },
            'total_objects': self.page.paginator.count,  # Total number of objects in the queryset
            'total_pages': self.page.paginator.num_pages,  # Total number of pages available
            'results': data  # Serialized results for the current page
        })

# ======================================================================================================================