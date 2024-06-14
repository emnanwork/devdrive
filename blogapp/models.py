from django.db import models
from django.conf import settings

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=25)
    
    def __str__(self):
        return self.title
    
class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="blogs")
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
    body = models.TextField()
    thumpnail = models.ImageField(upload_to="img")
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    is_important = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="blogs")
    
    def __str__(self):
        return self.title