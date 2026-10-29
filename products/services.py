"""Capa de servicios: aqui vive la logica de negocio (los descuentos).

Flujo: urls.py -> views.py -> services.py -> models.py
La vista no calcula nada: le pide el resultado a este modulo, y este modulo
consulta los datos a traves de los modelos.
"""
import unicodedata
from abc import ABC, abstractmethod
from decimal import ROUND_HALF_UP, Decimal

from django.shortcuts import get_object_or_404

from .models import Product

CENTAVOS = Decimal('0.01')


# --- Patron Strategy: cada regla de descuento es una clase intercambiable ---
class DescuentoStrategy(ABC):
    """Interfaz comun: recibe el precio y devuelve el precio ya con descuento."""
    nombre = 'Sin descuento'

    @abstractmethod
    def aplicar(self, precio):
        ...


class SinDescuento(DescuentoStrategy):
    def aplicar(self, precio):
        return precio


class DescuentoElectronica(DescuentoStrategy):
    nombre = 'Descuento del 10% en Electronica'

    def aplicar(self, precio):
        return precio * Decimal('0.90')


class DescuentoRopa(DescuentoStrategy):
    nombre = 'Descuento del 20% en Ropa'

    def aplicar(self, precio):
        return precio * Decimal('0.80')


# Estrategia de cada categoria (clave: nombre en minusculas y sin acentos)
ESTRATEGIAS = {
    'electronica': DescuentoElectronica(),
    'ropa': DescuentoRopa(),
}


def _normalizar(nombre):
    """'Electrónica ' -> 'electronica' (sin acentos, espacios ni mayusculas)."""
    sin_acentos = unicodedata.normalize('NFD', nombre).encode('ascii', 'ignore')
    return sin_acentos.decode().strip().lower()


def obtener_estrategia(categoria):
    """Elige la estrategia segun la categoria; si no tiene una, no hay descuento."""
    return ESTRATEGIAS.get(_normalizar(categoria.name), SinDescuento())


# --- Servicio que usa la vista ---
def calcular_precio_final(producto_id):
    """Devuelve el precio de un producto con el descuento de su categoria."""
    productos = Product.objects.select_related('category')
    producto = get_object_or_404(productos, pk=producto_id)
    estrategia = obtener_estrategia(producto.category)
    precio_final = estrategia.aplicar(producto.price).quantize(CENTAVOS, ROUND_HALF_UP)
    return {
        'producto': producto.name,
        'categoria': producto.category.name,
        'estrategia': estrategia.nombre,
        'precio_original': producto.price,
        'descuento': producto.price - precio_final,
        'precio_final': precio_final,
    }
