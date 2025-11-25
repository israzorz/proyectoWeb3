from django import forms
from .models import Cancha, TipoActividad, Reserva
from django.contrib.auth.models import User
# -------------------------
# Cancha Form
# -------------------------
class CanchaForm(forms.ModelForm):
    class Meta:
        model = Cancha
        fields = ['nombre', 'capacidad', 'estado']  # ← precio removido
        labels = {
            'nombre': 'Nombre',
            'capacidad': 'Capacidad',
            'estado': 'Estado',
        }

# -------------------------
# TipoActividad Form
# -------------------------
class TipoActividadForm(forms.ModelForm):
    class Meta:
        model = TipoActividad
        fields = ['nombre', 'descripcion', 'precioporHora']  # ← precio añadido aquí
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'precioporHora': 'Precio por Hora',
        }

# -------------------------
# Reserva Form
# -------------------------
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['id_cancha', 'id_usuario', 'id_actividad', 'fecha', 'hora_inicio', 'hora_fin']
        labels = {
            'id_cancha': 'Cancha',
            'id_usuario': 'Usuario',
            'id_actividad': 'Actividad',
            'fecha': 'Fecha',
            'hora_inicio': 'Hora de Inicio',
            'hora_fin': 'Hora de Fin',
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
        }

class UsuarioForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=False)
    telefono = forms.CharField(max_length=20, required=False)
    ci = forms.CharField(max_length=10, required=False)