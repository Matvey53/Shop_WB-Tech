from rest_framework.viewsets import ModelViewSet

from products.models import Product
from products.permissions import IsAdminOrReadOnly
from products.serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
