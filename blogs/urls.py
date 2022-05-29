from django.urls import path

from .views import (
    BlogListView,
    BlogDetailView,
    BlogLikeView,
    BlogCommentView
)


urlpatterns = [
    # listing all the blogs
    path('', BlogListView.as_view(), name='blog-list'),

    # detail view of a blog
    path('b/<int:blog_id>/', BlogDetailView.as_view(), name='blog-detail'),

    # liking a blog
    path('b/<int:blog_id>/like/', BlogLikeView.as_view(), name='blog-like'),

    # commenting on a blog
    path('b/<int:blog_id>/comment/', BlogCommentView.as_view(), name='blog-comment'),
]