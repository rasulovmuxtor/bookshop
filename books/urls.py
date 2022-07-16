from django.urls import path

from books import views

urlpatterns = [
    path('categories/', views.CategoryListAPIView.as_view(),
         name='category-list'),
    path('authors/', views.AuthorListAPIView.as_view(), name='category-list'),
    path('rate/', views.BookRatingCreateAPIView.as_view(), name='rate'),
    path('', views.BookListAPIView.as_view(), name='book-list'),
    path('<str:slug>/', views.BookRetrieveAPIView.as_view(),
         name='book-retrieve'),
]
