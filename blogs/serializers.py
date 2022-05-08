from unicodedata import category
from rest_framework import serializers

from .models import Blog, Image, Category


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)


"""
List serializer for the Blog model
"""
class BlogListSerializer(serializers.ModelSerializer):
    # adding image field to the serializer
    images = ImageSerializer(many=True, required=False)
    author = serializers.ReadOnlyField(source='author.name')
    comment_count = serializers.ReadOnlyField(source='comment_set.count')
    like_count = serializers.ReadOnlyField(source='like_set.count')
    category = serializers.CharField(source='category.name')
    class Meta:
        model = Blog
        fields = (
            'id',
            'category',
            'title', 
            'author', 
            'pub_date', 
            'body', 
            'images',
            'author',
            'comment_count',
            'like_count',
        )
        read_only_fields = ('id', 'pub_date')

    def create(self, validated_data):
        # poping the images data from the request data
        images_data = self.context['request'].data.pop('images')
        # poping the category data from the validated data
        category = validated_data.pop('category')['name']

        # creating the blog instance
        blog = Blog.objects.create(**validated_data, category=Category.objects.get(name=category))
        # return blog
        blog.save()

        # adding images to the blog
        for image_data in images_data:
            print(image_data)
            Image.objects.create(blog=blog, image=image_data)
        return blog

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images')
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        for image_data in images_data:
            Image.objects.update_or_create(blog=instance, image = image_data)
        return instance

