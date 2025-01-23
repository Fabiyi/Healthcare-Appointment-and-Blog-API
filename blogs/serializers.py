from rest_framework import serializers
from .models import Blog



class BlogSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.first_name')

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'author', 'author_name', 'created_at', 'updated_at']
        read_only_fields = ['author']
