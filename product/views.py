from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from product import models, serializers


class ProductListAPIView(ListAPIView):
    queryset = models.Product.objects.filter(is_active=True)
    serializer_class = serializers.ProductListSerializer
    search_fields = ('title', 'author__full_name', 'category__title')
    filterset_fields = ('author_id', 'category_id', 'category__slug')
    ordering_fields = ('rating', 'total_in_stock', 'published_year')
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)


class ProductRetrieveAPIView(RetrieveAPIView):
    queryset = models.Product.objects.filter(is_active=True)
    serializer_class = serializers.ProductSerializer
    lookup_field = 'slug'


class CategoryListAPIView(ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    search_fields = ('title',)


class AuthorListAPIView(ListAPIView):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    search_fields = ('full_name',)


class ProductRatingCreateAPIView(CreateAPIView):
    queryset = models.ProductRating.objects.all()
    serializer_class = serializers.ProductRatingSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)
