from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Usuario, Cancha, TipoActividad, Reserva

# Crear un inline para el modelo Usuario (campos extra)
class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = 'Información adicional'
    fk_name = 'user'

# Extender UserAdmin para incluir el inline
class UserAdmin(BaseUserAdmin):
    inlines = (UsuarioInline,)

# Primero remover el User original para registrar el personalizado
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Registrar los otros modelos normalmente
admin.site.register(Cancha)
admin.site.register(TipoActividad)
admin.site.register(Reserva)
