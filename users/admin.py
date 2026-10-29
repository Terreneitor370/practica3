from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'telefono', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'telefono')
    ordering = ('email',)
    # El campo extra aparece al editar y al crear un usuario en el admin
    fieldsets = UserAdmin.fieldsets + (('Datos adicionales', {'fields': ('telefono',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos adicionales', {'fields': ('email', 'telefono')}),
    )
