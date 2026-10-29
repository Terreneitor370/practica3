from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Category, Product

# Rutas de la API (api/v1/ en tienda_online/urls.py + router de products/urls.py)
CATEGORIES_URL = '/api/v1/categories/'
PRODUCTS_URL = '/api/v1/products/'


class CategoryTestCase(TestCase):
    def setUp(self):
        # Usuario de prueba autenticado en el cliente (opcion A de la practica)
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', password='test123')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Electronica')

    def test_create_category(self):
        response = self.client.post(CATEGORIES_URL, {'name': 'Ropa'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Ropa')
        self.assertEqual(Category.objects.count(), 2)

    def test_list_categories(self):
        response = self.client.get(CATEGORIES_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Electronica')


class ProductTestCase(TestCase):
    def setUp(self):
        # ProductViewSet usa IsAuthenticated, por eso se autentica al usuario de prueba
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', password='test123')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Electronica')
        self.product = Product.objects.create(
            name='Laptop',
            category=self.category,
            description='Laptop HP',
            price=15000.00
        )

    def test_create_product(self):
        response = self.client.post(PRODUCTS_URL, {
            'name': 'Mouse',
            'category': self.category.id,
            'description': 'Mouse inalambrico',
            'price': 500.00
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)
        mouse = Product.objects.get(name='Mouse')
        self.assertEqual(mouse.category, self.category)

    def test_list_products(self):
        response = self.client.get(PRODUCTS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Laptop')
        # La API muestra el nombre de la categoria, no el id (Practica 3)
        self.assertEqual(response.data[0]['category'], 'Electronica')

    def test_update_product(self):
        response = self.client.put(f'{PRODUCTS_URL}{self.product.id}/', {
            'name': 'Laptop Pro',
            'category': self.category.id,
            'description': 'Laptop HP actualizada',
            'price': 18000.00
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Laptop Pro')
        self.assertEqual(self.product.price, Decimal('18000.00'))

    def test_delete_product(self):
        response = self.client.delete(f'{PRODUCTS_URL}{self.product.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)


class PrecioFinalTestCase(TestCase):
    def setUp(self):
        # Cliente sin autenticar: cada prueba decide si manda o no el token JWT
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', password='test123')
        electronica = Category.objects.create(name='Electronica')
        ropa = Category.objects.create(name='Ropa')
        self.laptop = Product.objects.create(
            name='Laptop',
            category=electronica,
            description='Laptop HP',
            price=15000.00
        )
        self.playera = Product.objects.create(
            name='Playera',
            category=ropa,
            description='Playera de algodon',
            price=500.00
        )

    def test_precio_final_con_token(self):
        # Se pide un JWT real en /token/ y se manda en el header Authorization
        datos = {'username': 'test', 'password': 'test123'}
        login = self.client.post('/api/v1/token/', datos, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")

        # Dos productos de categorias distintas: cada una aplica su propia estrategia
        laptop = self.client.get(f'{PRODUCTS_URL}{self.laptop.id}/precio-final/')
        self.assertEqual(laptop.status_code, 200)
        self.assertEqual(laptop.data['precio_final'], '13500.00')  # Electronica -10%
        playera = self.client.get(f'{PRODUCTS_URL}{self.playera.id}/precio-final/')
        self.assertEqual(playera.status_code, 200)
        self.assertEqual(playera.data['precio_final'], '400.00')  # Ropa -20%

    def test_precio_final_sin_token(self):
        response = self.client.get(f'{PRODUCTS_URL}{self.laptop.id}/precio-final/')
        self.assertEqual(response.status_code, 401)
