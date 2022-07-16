from rest_framework import serializers

from books import models


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'full_name')
        model = models.Author


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'slug')
        model = models.Category


class BookListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        fields = ('id', 'title', 'author', 'slug', 'image',
                  'price', 'discount_price', 'published_year',
                  'rating')
        model = models.Book


class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = AuthorSerializer()

    class Meta:
        fields = ('id', 'title', 'author', 'category', 'slug', 'image',
                  'price', 'discount_price', 'published_year',
                  'rating', 'total_in_stock', 'description')
        model = models.Book


class BookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'book', 'rating', 'comment')
        model = models.BookRating
