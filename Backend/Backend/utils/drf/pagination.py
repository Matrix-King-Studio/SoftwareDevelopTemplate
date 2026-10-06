"""
统一分页工具。

本项目所有列表接口统一使用 ``StandardPageNumberPagination`` 分页。

分页请求参数:
- ``page``：页码,默认 1
- ``page_size``：每页条数,默认 20,最大 100

分页响应结构(嵌入在统一响应的 data 字段中)::

    {
        "count": 100,      # 总记录数
        "page": 1,         # 当前页码
        "page_size": 20,   # 当前每页条数
        "results": [...],  # 当前页数据列表
    }
"""

from rest_framework.pagination import PageNumberPagination


class StandardPageNumberPagination(PageNumberPagination):
    """输出与接口文档一致的分页结构。

    - ``page_size``：默认每页 20 条
    - ``page_size_query_param``：前端通过 ``page_size`` 参数自定义每页条数
    - ``max_page_size``：每页最大 100 条,防止恶意大量请求
    """

    page_size = 20
    page_size_query_param = "page_size"
    page_query_param = "page"
    max_page_size = 100

    def get_paginated_data(self, data):
        """构建统一分页数据字典,由 ``StandardAPIView.paginate()`` 包进统一响应 data。"""
        return {
            "count": self.page.paginator.count,
            "page": self.page.number,
            "page_size": self.get_page_size(self.request),
            "results": data,
        }
