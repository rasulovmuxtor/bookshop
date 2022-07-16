from django.urls import path

from order import views

urlpatterns = [
    path('', views.OrderAPIView.as_view(), name='order'),
    path('cart/', views.CartProductCreateAPIView.as_view(), name='cart'),

]
