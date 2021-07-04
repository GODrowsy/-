from __future__ import unicode_literals
from django.contrib import admin

from .models import *

# Register your models here.
# 自定义显示效果类
class WorkDateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_id', 'name', 'firsttime', 'lasttime', 'date']


# 注册模型类
admin.site.register(WorkDate, WorkDateAdmin)