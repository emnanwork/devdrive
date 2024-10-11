from rest_framework import serializers
from blogapp.models import Blog, Comment
from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model


class BlogSerializer(serializers.ModelSerializer):
    # user = MainUserSerializer(read_only=True)
    # related_blog = serializers.SerializerMethodField(method_name="related_blogs")
    class Meta:
        model = Blog
        fields = ['id', 'user', 'title', 'slug', 'body', 'thumpnail', 'created',
                  'updated', 'category', 'featured']
        



class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = get_user_model()
        fields = ['id', 'email', 'username', 'address', 'phone', 'role', 'bio', 'profile_pic']
        
    
 


    