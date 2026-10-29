from rest_framework import serializers
from .models import Category, Product

class ProductSerializer(serializers.ModelSerializer):
    # StringRelatedField es solo lectura: aqui se recibe el id de la categoria
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'category')
        # fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = str(instance.category) # Muestra el nombre, no el ID
        return data

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')

class PrecioFinalSerializer(serializers.Serializer):
    # Respuesta de /precio-final/: los montos salen como texto con 2 decimales
    producto = serializers.CharField()
    categoria = serializers.CharField()
    estrategia = serializers.CharField()
    precio_original = serializers.DecimalField(max_digits=10, decimal_places=2)
    descuento = serializers.DecimalField(max_digits=10, decimal_places=2)
    precio_final = serializers.DecimalField(max_digits=10, decimal_places=2)

