from django.urls import path

from product import views

urlpatterns = [
    path('categories/', views.CategoryListAPIView.as_view(),
         name='category-list'),
    path('authors/', views.AuthorListAPIView.as_view(), name='category-list'),
    path('rate/', views.ProductRatingCreateAPIView.as_view(), name='rate'),
    path('', views.ProductListAPIView.as_view(), name='product-list'),
    path('<str:slug>/', views.ProductRetrieveAPIView.as_view(),
         name='product-retrieve'),
]
