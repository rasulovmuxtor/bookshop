from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from order.models import OrderProduct
from product import models, serializers


class ProductListAPIView(ListAPIView):
    queryset = models.Product.objects.active()
    serializer_class = serializers.ProductListSerializer
    search_fields = ('title', 'author__full_name', 'category__title')
    filterset_fields = ('author_id', 'category_id', 'category__slug')
    ordering_fields = ('rating', 'total_in_stock', 'published_year')
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)


class RecommendedProductListAPIView(ProductListAPIView):
    def get_queryset(self):
        queryset = super().get_queryset()
        category_ids = self.get_category_ids()
        return queryset.filter(category_id__in=category_ids)

    def get_category_ids(self):
        # TODO
        """category_ids will be cached"""
        user = self.request.user
        q = OrderProduct.objects.filter(order__user_id=user.id).annotate(
            category_id=F('product__category_id'))

        q = q.order_by('category_id').distinct('category_id')
        return q.values_list('category_id', flat=True)


class ProductRetrieveAPIView(RetrieveAPIView):
    queryset = models.Product.objects.active()
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
