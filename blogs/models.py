from django.db import models
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save

from .utils import unique_slug_generator
from accounts.models import Account



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # customize save method to automatically create slug
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name




class Blog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title
        

class Image(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    
    def __str__(self):
        return self.image.__str__()


# Model for the post comments
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=200)
    commented_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['commented_at']

    def __str__(self):
        return self.comment


# Model for the post likes
class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    # a user can only like a post once
    class Meta:
        unique_together = ('blog', 'account')
        ordering = ['-liked_at']

    def __str__(self):
        return self.account.username


# signal to create slug after saving the blog
@receiver(post_save, sender=Blog)
def create_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()
