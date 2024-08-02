from rest_framework import serializers
from blogapp.models import Blog, Comment


class BlogSerializer(serializers.ModelSerializer):
    # user = MainUserSerializer(read_only=True)
    # related_blog = serializers.SerializerMethodField(method_name="related_blogs")
    class Meta:
        model = Blog
        fields = ['id', 'user', 'title', 'slug', 'body', 'thumpnail', 'created',
                  'updated', 'category', 'featured']
        
    
    