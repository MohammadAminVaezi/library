from rest_framework import serializers
from .models import Author, Book, Comment


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = (
            'id',
            'firstname',
            'lastname',
            'nationality'
        )
        read_only_fields = ('id',)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'cover',
            'author',
            'genre',
            'summary',
            'rate',
            'published_at',
            'view_count'
        )
        read_only_fields = (
            'rate',
            'view_count',
            'id'
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'book',
            'text',
            'rating'
        )
        read_only_fields = ('user', 'id')

    def create(self, validated_data):
        user = self.context['user']
        validated_data["user"] = user
        instance = super().create(validated_data)
        return instance
