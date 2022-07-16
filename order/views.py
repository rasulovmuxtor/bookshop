from rest_framework.generics import CreateAPIView, ListCreateAPIView

from order import models, serializers


class CartProductCreateAPIView(CreateAPIView):
    """
    NOTE: To delete product from cart send quantity=0
    """
    queryset = models.CartProduct.objects.all()
    serializer_class = serializers.CartProductSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


class OrderAPIView(ListCreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        q = super().get_queryset()
        return q.filter(user_id=self.request.user.id)
