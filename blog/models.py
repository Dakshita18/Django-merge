from django.db import models
from autoslug import AutoSlugField

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=15, blank=True, null=True,unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    password = models.CharField(max_length=200)
    def __str__(self):
        return self.username
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True, max_length=255)

def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True, max_length=255)

    def __str__(self):
        return self.name
    



class Post(models.Model):
    category =models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    tag= models.ManyToManyField(Tag,null=True,blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    profile_pictures = models.ImageField(upload_to='profile_pics/',blank=True, null=True)
    icon=models.ImageField(upload_to='icon/',blank=True, null=True)
    def publish(self):
        self.published_date = timezone.now()
        self.save()


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}: {self.text[:30]}"

    def children(self):
        return Comment.objects.filter(parent=self).order_by('id')

    @property
    def is_parent(self):
        return self.parent is None
    




