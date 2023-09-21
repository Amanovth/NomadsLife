from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class GuaranteedToursPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100
