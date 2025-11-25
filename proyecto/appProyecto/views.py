from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout , authenticate
from django.contrib import admin
from django.contrib import messages
from .models import Cancha, TipoActividad, Reserva, Usuario 
from .forms import CanchaForm, TipoActividadForm, ReservaForm, UsuarioForm
from django.contrib.auth.models import User
import datetime
from datetime import time
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test

#admin 12345
#usuario1 12345

def admin_required(user):
    return user.is_superuser

def panel_admin(request):
    return render(request, 'panel_admin.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')  # Redirige a la pantalla principal después del login
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return redirect('login')
    return render(request, 'login.html')


# Logout personalizado
def logout_view(request):
    logout(request)
    return redirect('login')


# Pantalla de inicio tras login
def inicio(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'inicio.html')

def lista_canchas(request):
    canchas = Cancha.objects.all()
    return render(request, 'lista_canchas.html', {'canchas': canchas})

# Crear nueva cancha
def crear_cancha(request):
    if request.method == 'POST':
        form = CanchaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_canchas')
    else:
        form = CanchaForm()
    return render(request, 'cancha_form.html', {'form': form})

# Editar cancha
def editar_cancha(request, pk):
    cancha = get_object_or_404(Cancha, pk=pk)
    if request.method == 'POST':
        form = CanchaForm(request.POST, instance=cancha)
        if form.is_valid():
            form.save()
            return redirect('lista_canchas')
    else:
        form = CanchaForm(instance=cancha)
    return render(request, 'cancha_form.html', {'form': form})

# Eliminar cancha
def eliminar_cancha(request, pk):
    cancha = get_object_or_404(Cancha, pk=pk)
    if request.method == 'POST':
        cancha.delete()
        return redirect('lista_canchas')
    return render(request, 'cancha_borrado.html', {'cancha': cancha})


def lista_actividades(request):
    actividades = TipoActividad.objects.all()
    return render(request, 'lista_actividades.html', {'actividades': actividades})

def crear_actividad(request):
    if request.method == 'POST':
        form = TipoActividadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_actividades')
    else:
        form = TipoActividadForm()
    return render(request, 'actividad_form.html', {'form': form})

def editar_actividad(request, pk):
    actividad = get_object_or_404(TipoActividad, pk=pk)
    if request.method == 'POST':
        form = TipoActividadForm(request.POST, instance=actividad)
        if form.is_valid():
            form.save()
            return redirect('lista_actividades')
    else:
        form = TipoActividadForm(instance=actividad)
    return render(request, 'actividad_form.html', {'form': form})

def eliminar_actividad(request, pk):
    actividad = get_object_or_404(TipoActividad, pk=pk)
    if request.method == 'POST':
        actividad.delete()
        return redirect('lista_actividades')
    return render(request, 'actividad_borrado.html', {'actividad': actividad})


# -------------------------
# Reserva CRUD
# -------------------------

def lista_reservas(request):
    reservas = Reserva.objects.select_related('id_cancha', 'id_usuario', 'id_actividad').all()
    return render(request, 'lista_reservas.html', {'reservas': reservas})
def crear_reserva(request):
    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_reservas")
    else:
        form = ReservaForm()

    return render(request, "reserva_form.html", {
        "form": form
    })

def editar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('lista_reservas')
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'reserva_form.html', {'form': form})

def eliminar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        reserva.delete()
        return redirect('lista_reservas')
    return render(request, 'reserva_borrado.html', {'reserva': reserva})

#CRUD USUARIO
def lista_usuarios(request):
    usuarios = Usuario.objects.select_related('user').all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            Usuario.objects.create(
                user=user,
                telefono=form.cleaned_data['telefono'],
                ci=form.cleaned_data['ci']
            )
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'crear_usuario.html', {'form': form})

def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario.user.username = form.cleaned_data['username']
            if form.cleaned_data['password']:
                usuario.user.set_password(form.cleaned_data['password'])
            usuario.user.email = form.cleaned_data['email']
            usuario.user.save()
            usuario.telefono = form.cleaned_data['telefono']
            usuario.ci = form.cleaned_data['ci']
            usuario.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(initial={
            'username': usuario.user.username,
            'email': usuario.user.email,
            'telefono': usuario.telefono,
            'ci': usuario.ci
        })
    return render(request, 'crear_usuario.html', {'form': form})

@login_required
@user_passes_test(admin_required)
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.user.delete()  # elimina también auth_user
        return redirect('lista_usuarios')
    return render(request, 'eliminar_usuario.html', {'usuario': usuario})




def consultar_disponibilidad(request):
    canchas = Cancha.objects.all()
    cancha_id = request.GET.get("cancha_id")
    fecha = request.GET.get("fecha")

    disponibilidad = []

    if cancha_id and fecha:
        # Crear intervalos de hora de 7:00 a 23:00
        for h in range(7, 24):
            inicio = datetime.time(h, 0)
            fin = datetime.time(h+1, 0) if h < 23 else datetime.time(0, 0)  # 23:00-24:00
            intervalo = f"{inicio.strftime('%H:%M')} - {fin.strftime('%H:%M') if h<23 else '24:00'}"

            # Buscar si hay reserva que se solape con este intervalo
            reservas = Reserva.objects.filter(id_cancha=cancha_id, fecha=fecha)
            estado = "Disponible"
            actividad = ""
            usuario = ""
            ci = ""

            for r in reservas:
                # convertir tiempos a minutos para comparación simple
                def to_minutes(t):
                    return t.hour*60 + t.minute
                start_slot = to_minutes(inicio)
                end_slot = to_minutes(fin) if h < 23 else 24*60
                start_res = to_minutes(r.hora_inicio)
                end_res = to_minutes(r.hora_fin) if r.hora_fin != datetime.time(0,0) else 24*60

                # solapamiento
                if start_res < end_slot and end_res > start_slot:
                    estado = "Reservado"
                    actividad = r.id_actividad.nombre
                    usuario = r.id_usuario.user.username
                    ci = r.id_usuario.ci
                    break

            disponibilidad.append({
                "hora": intervalo,
                "estado": estado,
                "actividad": actividad,
                "usuario": usuario,
                "ci": ci
            })

    return render(request, "consultar_disponibilidad.html", {
        "canchas": canchas,
        "cancha_seleccionada": cancha_id,
        "fecha": fecha,
        "disponibilidad": disponibilidad,
    })

def consultar_disponibilidad_api(request):
    """
    API que recibe GET params: cancha_id (int) y fecha (YYYY-MM-DD)
    Devuelve JSON con los horarios de 7 a 23 y su estado ("Disponible" / "Reservado").
    """
    cancha_id = request.GET.get('cancha_id')
    fecha_str = request.GET.get('fecha')

    # Validaciones básicas
    if not cancha_id or not fecha_str:
        return JsonResponse({'error': 'cancha_id y fecha son requeridos.'}, status=400)

    try:
        cancha = Cancha.objects.get(pk=cancha_id)
    except Cancha.DoesNotExist:
        return JsonResponse({'error': 'Cancha no encontrada.'}, status=404)

    try:
        fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Formato de fecha inválido (usar YYYY-MM-DD).'}, status=400)

    # Obtener reservas para esa cancha y fecha
    reservas = Reserva.objects.filter(id_cancha=cancha, fecha=fecha)

    # Generar slots de horas: 7..23 (cada slot es [H:00, H+1:00))
    horarios = []
    for h in range(7, 24):  # 7 a 23 inclusive -> slots 7-8 ... 23-24 (mostramos hasta 23)
        slot_start = datetime.time(hour=h, minute=0, second=0)
        slot_end_hour = h + 1
        # slot_end_hour puede ser 24 -> python time acepta 0..23, así que para 24 usamos 00:00 del día siguiente
        if slot_end_hour == 24:
            slot_end = datetime.time(hour=0, minute=0, second=0)
        else:
            slot_end = datetime.time(hour=slot_end_hour, minute=0, second=0)

        estado = 'Disponible'
        # Comprobar solapamiento con cualquier reserva
        for r in reservas:
            # r.hora_inicio y r.hora_fin son objetos datetime.time
            # Condición de solapamiento entre (slot_start, slot_end) y (r.hora_inicio, r.hora_fin):
            # overlap si r.hora_inicio < slot_end AND r.hora_fin > slot_start
            # Necesitamos tratar el caso fin == 00:00 como 24:00 si reserva cruza medianoche (raro para tu caso)
            r_start = r.hora_inicio
            r_end = r.hora_fin

            # Normalizar reservas que terminen a 00:00 como 24:00 para comparación simple:
            def time_to_minutes(t):
                return t.hour * 60 + t.minute

            slot_start_m = time_to_minutes(slot_start)
            # si slot_end es 00:00 (midnight) interpretarlo como 24*60
            slot_end_m = 24 * 60 if slot_end.hour == 0 and slot_end.minute == 0 else time_to_minutes(slot_end)
            r_start_m = time_to_minutes(r_start)
            r_end_m = 24 * 60 if (r_end.hour == 0 and r_end.minute == 0) else time_to_minutes(r_end)

            # Overlap:
            if (r_start_m < slot_end_m) and (r_end_m > slot_start_m):
                estado = 'Reservado'
                break

        horarios.append({
            'hora': f"{h:02d}:00 - {h+1:02d}:00" if h < 23 else f"{h:02d}:00 - 24:00",
            'hour': h,
            'estado': estado
        })

    return JsonResponse({'fecha': fecha_str, 'cancha': cancha.nombre, 'horarios': horarios})
