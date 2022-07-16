from rest_framework import serializers

from product import models


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'full_name')
        model = models.Author


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'slug')
        model = models.Category


class ProductListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        fields = ('id', 'title', 'author', 'slug', 'image',
                  'price', 'discount_price', 'published_year',
                  'rating')
        model = models.Product


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = AuthorSerializer()

    class Meta:
        fields = ('id', 'title', 'author', 'category', 'slug', 'image',
                  'price', 'discount_price', 'published_year',
                  'rating',  'description')
        model = models.Product


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'product', 'rating', 'comment')
        model = models.ProductRating
