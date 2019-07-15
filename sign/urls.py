#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: WangLX
# datetime: 2019/6/3 23:44
# software: PyCharm

from django.urls import path
from sign import views_if

urlpatterns = [
    # sign system interface:
    # ex: /api/add_event/
    path('api/add_event/', views_if.add_event, name='add_event'),
    # ex: /api/add_guest/
    path('api/add_guest/', views_if.add_guest, name='add_guest'),
    # ex: /api/get_event_list/
    path('api/get_event_list/', views_if.get_event_list, name='get_event_list'),
    # ex: /api/get_guest_list/
    path('api/get_guest_list/', views_if.get_guest_list, name='get_guest_list'),
    # ex: /api/user_sign/
    path('api/user_sign/', views_if.user_sign, name='user_sign'),

]
