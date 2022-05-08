from multiprocessing import context
from unicodedata import category
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Blog, Category, Comment, Like
from .serializers import BlogListSerializer, ImageSerializer
from .paginations import CustomLimitOffsetPagination


class BlogListView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer
    pagination_class = CustomLimitOffsetPagination
    permission_classes = (AllowAny,)

    # customizing the queryset to get the parameters from the url
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        print(category)
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset


class BlogCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = BlogListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

