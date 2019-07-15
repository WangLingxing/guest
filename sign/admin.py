from django.contrib import admin

# Register your models here.
import sign
from sign.models import Event, Guest


class EventAdmin(admin.ModelAdmin):
    """
    admin model字段显示,搜索栏，过滤器
    """
    list_display = ['id', 'name', 'status', 'address', 'start_time']
    search_fields = ['name']
    list_filter = ['status']


class GuestAdmin(admin.ModelAdmin):
    """
    admin model字段显示,搜索栏，过滤器
    """
    list_display = ['realname', 'phone', 'email', 'sign', 'create_time', 'event']
    search_fields = ['realname', 'phone']
    list_filter = ['sign']

admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)
