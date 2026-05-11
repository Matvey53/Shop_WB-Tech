from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from cart.models import CartItem
from orders.models import Order
from products.models import Product

User = get_user_model()


class ShopAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            email='user@mail.com',
            password='test123',
            balance=Decimal('1000.00'),
        )

        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@mail.com',
            password='admin123',
        )

        self.product = Product.objects.create(
            name='iPhone',
            description='phone',
            price=Decimal('100.00'),
            stock=10,
        )

    def test_user_registration(self):
        response = self.client.post(
            '/api/auth/register/',
            {
                'username': 'new_user',
                'email': 'new@mail.com',
                'password': 'testpass123',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='new_user').exists())

    def test_admin_can_create_product(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            '/api/products/',
            {
                'name': 'MacBook',
                'description': 'Laptop',
                'price': '500.00',
                'stock': 5,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name='MacBook').exists())

    def test_regular_user_cannot_create_product(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            '/api/products/',
            {
                'name': 'MacBook',
                'description': 'Laptop',
                'price': '500.00',
                'stock': 5,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_add_product_to_cart(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            '/api/cart/',
            {
                'product': self.product.id,
                'quantity': 2,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)

        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.user, self.user)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)

    def test_create_order_from_cart(self):
        self.client.force_authenticate(user=self.user)

        CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2,
        )

        response = self.client.post('/api/orders/create/')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.user.refresh_from_db()
        self.product.refresh_from_db()

        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(CartItem.objects.count(), 0)
        self.assertEqual(self.user.balance, Decimal('800.00'))
        self.assertEqual(self.product.stock, 8)
