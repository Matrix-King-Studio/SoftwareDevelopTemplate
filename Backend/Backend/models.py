from django.db import models


class BaseModel(models.Model):
    """基础模型"""

    created_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    is_delete = models.BooleanField(verbose_name="是否删除", default=False)

    class Meta:
        abstract = True
