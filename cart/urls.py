from rest_framework.routers import DefaultRouter

from cart.views import CartItemViewSet

router = DefaultRouter()
router.register('', CartItemViewSet, basename='cart')

urlpatterns = router.urls
