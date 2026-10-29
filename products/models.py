from django.db import models

#Modelo de categoria
class Category(models.Model):
    name = models.CharField(max_length=225, verbose_name='Nombre')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    def __str__(self):
        return self.name

#Modelo de producto
class Product(models.Model):
    name = models.CharField(max_length=225, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripcion')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='get_products', verbose_name='Category')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']
    def __str__(self):
        return self.name

    @classmethod
    def crear_con_categoria_default(cls, name, description, price):
        """Factory Method: crea un producto en la categoria por defecto ('General').

        Si esa categoria todavia no existe, la crea; asi se puede dar de alta un
        producto sin elegir (ni crear) una categoria antes.
        """
        categoria = Category.objects.filter(name='General').first()
        if categoria is None:
            categoria = Category.objects.create(name='General')
        return cls.objects.create(
            name=name,
            description=description,
            price=price,
            category=categoria
        )