from multiprocessing import context
from unicodedata import category
from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import AuthenticationFailed

from .models import Blog, Category, Comment, Like
from .serializers import BlogListSerializer, BlogDetailSerializer, CommentSerializer
from .paginations import CustomLimitOffsetPagination


class BlogListView(APIView, CustomLimitOffsetPagination):
    # queryset = Blog.objects.all()
    # serializer_class = BlogListSerializer
    # pagination_class = CustomLimitOffsetPagination
    # permission_classes = (AllowAny,)

    # customizing the queryset to get the parameters from the url
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     category = self.request.query_params.get('category', None)
    #     print(category)
    #     if category:
    #         queryset = queryset.filter(category__name=category)
    #     return queryset

    def get(self, request, *args, **kwargs):
        category = request.query_params.get('category', None)
        if category:
            blogs = Blog.objects.filter(category__name=category)
        else:
            blogs = Blog.objects.all()
        blog_page = self.paginate_queryset(blogs, request, view=self)
        serializer = BlogListSerializer(blog_page, many=True)
        
        return self.get_paginated_response(serializer.data)



class BlogCreateView(APIView):

    def post(self, request):
        print(request.data)
        serializer = BlogDetailSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDetailView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, slug):
        # getting the blog instance from the slug
        # if the blog is not found, raise an exception
        try:
            blog = Blog.objects.get(slug=slug)
        except Blog.DoesNotExist:
            return Response(
                {'error': 'Blog with slug {} does not exist'.format(slug)},
                status=status.HTTP_404_NOT_FOUND)
        serializer = BlogDetailSerializer(blog, context={'request': request})
        return Response(serializer.data)


class BlogUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    # view to update the blog
    def put(self, request, slug):
        # getting the blog from the slug
        # raising an exception if the blog does not exist
        try:
            blog = Blog.objects.get(slug=slug)
        except Blog.DoesNotExist:
            return Response(
                {'error': 'Blog with slug {} does not exist'.format(slug)},
                status=status.HTTP_404_NOT_FOUND)
        
        # checking if the user is the author of the blog
        if blog.author != request.user:
            return Response(
                {'error': 'You are not the author of the blog'},
                status=status.HTTP_403_FORBIDDEN)

        # passing the request.data to the serializer 
        serializer = BlogDetailSerializer(blog, data=request.data, context={'request': request})

        # checking if the serializer is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # view for deleting the blog
    def delete(self, request, slug):
        try:
            blog = Blog.objects.get(slug=slug)
        except Blog.DoesNotExist:
            return Response(
                {'error': 'Blog with slug {} does not exist'.format(slug)},
                status=status.HTTP_404_NOT_FOUND)

        # checking if the user is the author of the blog
        if blog.author == request.user:
            blog.delete()
        else:
            raise AuthenticationFailed('You are not the author of the blog')
        return Response(
            {'message': 'Blog " {} " has been deleted'.format(blog.title)},
            status=status.HTTP_204_NO_CONTENT
            )

class BlogLikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, slug):
        # getting the blog from the slug
        # raising an exception if the blog does not exist
        try:
            blog = Blog.objects.get(slug=slug)
        except Blog.DoesNotExist:
            return Response(
                {'error': 'Blog with slug {} does not exist'.format(slug)},
                status=status.HTTP_404_NOT_FOUND)

        # checking if the user has already liked the blog
        # disliking the blog if the user has already liked it
        if Like.objects.filter(blog=blog, account=request.user).exists():
            like = Like.objects.get(blog=blog, account=request.user)
            like.delete()
            return Response(
                {'liked': False},
                status=status.HTTP_200_OK)

        # liking the blog if the user has not liked it yet
        like = Like.objects.create(blog=blog, account=request.user)
        like.save()
        return Response(
            {'liked': True},
            status=status.HTTP_200_OK)


class BlogCommentView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, slug):
        # getting the blog from the slug
        # raising an exception if the blog does not exist
        try:
            blog = Blog.objects.get(slug=slug)
        except Blog.DoesNotExist:
            return Response(
                {'error': 'Blog with slug {} does not exist'.format(slug)},
                status=status.HTTP_404_NOT_FOUND)

        # passing the request.data to the serializer
        serializer = CommentSerializer(data=request.data, context={'request': request})
        
        # checking if the serializer is valid
        if serializer.is_valid():
            serializer.save(blog=blog, account=request.user)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            



