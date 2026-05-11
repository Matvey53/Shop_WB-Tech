from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from cart.models import CartItem
from cart.serializers import CartItemSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity},
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        response_serializer = self.get_serializer(cart_item)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )
