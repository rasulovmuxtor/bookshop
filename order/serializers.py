from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from order import models


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartProduct
        fields = ('id', 'product', 'quantity')

    def create(self, validated_data):
        quantity = validated_data.pop('quantity')
        instance, _ = models.CartProduct.objects.update_or_create(
            **validated_data, defaults={'quantity': quantity}
        )
        return instance


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ('id', 'status', 'payment_status', 'payment_type', 'address',
                  'latitude', 'longitude', 'delivery_price', 'total_price',
                  'order_price', 'created_at', 'modified_at')
        extra_kwargs = {
            'status': {'read_only': True},
            'payment_status': {'read_only': True},
            'delivery_price': {'read_only': True},
            'total_price': {'read_only': True},
            'order_price': {'read_only': True},
        }

    def create(self, validated_data):
        user = validated_data.get('user')
        cart_products = models.CartProduct.objects.filter(user_id=user.id,
                                                          quantity__gt=0)
        try:
            with transaction.atomic():
                instance = models.Order(total_price=0, order_price=0,
                                        **validated_data)
                instance.delivery_price = instance.get_delivery_price()
                instance.save()
                order_products = []
                for cart_product in cart_products.select_related('product'):
                    product = cart_product.product
                    if product.discount_price > 0:
                        price = product.discount_price
                    else:
                        price = product.price
                    order_product = models.OrderProduct(
                        order_id=instance.id,
                        product_id=product.id,
                        price=price,
                        quantity=cart_product.quantity
                    )

                    product.total_in_stock -= cart_product.quantity
                    product.save(update_fields=['total_in_stock'])

                    order_products.append(order_product)
                    instance.total_price += order_product.total_price

                models.OrderProduct.objects.bulk_create(order_products)
                instance.order_price = instance.get_order_price()
                instance.save(update_fields=['order_price', 'total_price'])
                # clear cart products
                cart_products.update(quantity=0)
        except:  # noqa
            raise serializers.ValidationError(
                {'message': _("something went wrong. try again.")})

        return instance
