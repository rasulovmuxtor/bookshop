from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from books import models, serializers


class BookListAPIView(ListAPIView):
    queryset = models.Book.objects.all().order_by('-rating')
    serializer_class = serializers.BookListSerializer
    search_fields = ('title', 'author__full_name', 'category__title')
    filterset_fields = ('author_id', 'category_id', 'category__slug')
    ordering_fields = ('rating', 'total_in_stock', 'published_year')
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)


class BookRetrieveAPIView(RetrieveAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    lookup_field = 'slug'


class CategoryListAPIView(ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    search_fields = ('title',)


class AuthorListAPIView(ListAPIView):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    search_fields = ('full_name',)


class BookRatingCreateAPIView(CreateAPIView):
    queryset = models.BookRating.objects.all()
    serializer_class = serializers.BookRatingSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)
