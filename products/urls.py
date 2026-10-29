from django.urls import path, include
from .views import CategoryViewSet, ProductViewSet, PrecioFinalView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('products/<int:pk>/precio-final/', PrecioFinalView.as_view(),
         name='precio_final'),
    path('', include(router.urls))
]
