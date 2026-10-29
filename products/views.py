from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated 
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import CategorySerializer, PrecioFinalSerializer, ProductSerializer
from .services import calcular_precio_final
# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated] # 2. Proteger el endpoint
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category'] # Permite /api/products/?category=1

class PrecioFinalView(APIView):
    """Facade: un solo GET oculta todo el trabajo de services.py y models.py."""
    permission_classes = [IsAuthenticated] # Protegido con JWT

    def get(self, request, pk):
        datos = calcular_precio_final(pk) # La logica vive en services.py
        return Response(PrecioFinalSerializer(datos).data)