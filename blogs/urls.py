from django.urls import path

from .views import (
    BlogListView,
    BlogCreateView,
)


urlpatterns = [
    path('', BlogListView.as_view(), name='blog-list'),
    path('create/', BlogCreateView.as_view(), name='blog-create'),
]