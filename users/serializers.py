from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    # write_only: la contrasena (hash) nunca sale en una respuesta de la API
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'telefono',
                  'password', 'is_active', 'is_staff']

    def validate(self, attrs):
        # La contrasena es obligatoria solo al crear; al editar es opcional
        if self.instance is None and not attrs.get('password'):
            raise serializers.ValidationError({'password': 'Este campo es requerido.'})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # guarda el hash, nunca el texto plano
        user.save()
        return user

    def update(self, instance, validated_data):
        # Solo se cambia la contrasena si viene en la peticion
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
