from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    telefono = models.CharField(max_length=20, blank=True, null=True)
    ci = models.CharField(max_length=10, blank=True, null=True)
    
    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.user.username


class Cancha(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('ocupada', 'Ocupada'),
        ('mantenimiento', 'Mantenimiento'),
    ]

    id_cancha = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    # ❌ eliminado: precioporHora
    # precioporHora = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'cancha'


# -------------------------
# TipoActividad
# -------------------------
class TipoActividad(models.Model):
    id_actividad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    # ✅ agregado PRECIO AQUÍ, como tú pediste
    precioporHora = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        db_table = 'tipoactividad'

    def __str__(self):
        return self.nombre


# -------------------------
# Reserva
# -------------------------
class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    id_cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    id_actividad = models.ForeignKey(TipoActividad, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        db_table = 'reserva'

    def __str__(self):
        return f"Reserva {self.id_reserva} - {self.id_cancha.nombre} - {self.id_usuario.user.username}"
