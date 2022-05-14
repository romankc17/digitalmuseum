from django.urls import path

from .views import (
    BlogListView,
    BlogCreateView,
    BlogDetailView,
    BlogUpdateView,
    BlogLikeView,
    BlogCommentView
)


urlpatterns = [
    # listing all the blogs
    path('', BlogListView.as_view(), name='blog-list'),

    # creating a new blog
    path('create/', BlogCreateView.as_view(), name='blog-create'),

    # detail view of a blog
    path('b/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),

    # updating and deleting a blog
    path('b/<slug:slug>/update/', BlogUpdateView.as_view(), name='blog-update'),

    # liking a blog
    path('b/<slug:slug>/like/', BlogLikeView.as_view(), name='blog-like'),

    # commenting on a blog
    path('b/<slug:slug>/comment/', BlogCommentView.as_view(), name='blog-comment'),
]