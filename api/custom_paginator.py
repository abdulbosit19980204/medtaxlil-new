from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10  # Bir sahifadagi yozuvlar soni
    page_size_query_param = 'limit'  # Frontend `limit` so‘rov parametriasini o‘zgartiradi
    page_query_param = 'page'  # Sahifa raqami uchun parametr (default: 'page')

    def get_paginated_response(self, data):
        return Response({
            'total_records': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link() is not None,
            'previous': self.get_previous_link() is not None,
            'data': data,
        })
