# helpers/paginations.py
from urllib.parse import urlparse, urlunparse

from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 10000

    def get_page_size(self, request):
        if request.query_params.get(self.page_size_query_param, "").lower() == "all":
            return None
        return super(CustomPageNumberPagination, self).get_page_size(request)

    def get_next_link(self):
        next_link = super(CustomPageNumberPagination, self).get_next_link()
        return self.replace_scheme(next_link)

    def get_previous_link(self):
        previous_link = super(CustomPageNumberPagination, self).get_previous_link()
        return self.replace_scheme(previous_link)

    def replace_scheme(self, link):
        # Replace http with https
        if link is not None:
            components = list(urlparse(link))
            components[0] = "https"
            return urlunparse(components)
        return None


class CustomPageNumberPagination100(CustomPageNumberPagination):
    page_size = 100
