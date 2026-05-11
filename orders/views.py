from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import Order
from orders.serializers import OrderSerializer
from orders.services import create_order_from_cart


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .prefetch_related('items__product')
            .order_by('-created_at')
        )

    @action(detail=False, methods=['post'], url_path='create')
    def create_from_cart(self, request):
        order = create_order_from_cart(request.user)
        serializer = self.get_serializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
