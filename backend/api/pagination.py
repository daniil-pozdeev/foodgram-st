from rest_framework.pagination import PageNumberPagination

from foodgram.constants import MAIN_PAGE_RECORDS_LIMIT


class MainPagePagination(PageNumberPagination):
    page_size_query_param = "limit"
    page_size = MAIN_PAGE_RECORDS_LIMIT
