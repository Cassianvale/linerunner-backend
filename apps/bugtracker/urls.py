#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


rouer = DefaultRouter()

rouer.register('bug',views.BugtrackerViewSet,basename='bugtracker')

urlpatterns = [
    path('bug',views.BugtrackerViewSet.as_view({"get":"query_name"})),
    path('bug/<int:pk>/',views.BugtrackerViewSet.as_view({"get":"retrieve"})),
    path('bug/create',views.BugtrackerViewSet.as_view({"post":"create"})),
    path('bug/<int:pk>/update',views.BugtrackerViewSet.as_view({"put":"update"})),
    path('bug/<int:pk>/delete',views.BugtrackerViewSet.as_view({"delete":"destroy"})),
]+rouer.urls
