"""
URL configuration for proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from appProyecto import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('inicio/', views.inicio, name='inicio'),
    path('panel-admin/', views.panel_admin, name='panel_admin'),

    path('admin/', admin.site.urls),
    path('canchas/', views.lista_canchas, name='lista_canchas'),
    path('canchas/crearCancha/', views.crear_cancha, name='crear_cancha'),
    path('canchas/editarCancha/<int:pk>/', views.editar_cancha, name='editar_cancha'),
    path('canchas/eliminarCancha/<int:pk>/', views.eliminar_cancha, name='eliminar_cancha'),

    #path('', include('proyecto.urls')),   
    
    # TipoActividad
    path('actividades/', views.lista_actividades, name='lista_actividades'),
    path('actividades/crear/', views.crear_actividad, name='crear_actividad'),
    path('actividades/editar/<int:pk>/', views.editar_actividad, name='editar_actividad'),
    path('actividades/eliminar/<int:pk>/', views.eliminar_actividad, name='eliminar_actividad'),

    # Reserva
    path('reservas/', views.lista_reservas, name='lista_reservas'),
    path('reservas/crear/', views.crear_reserva, name='crear_reserva'),
    path('reservas/editar/<int:pk>/', views.editar_reserva, name='editar_reserva'),
    path('reservas/eliminar/<int:pk>/', views.eliminar_reserva, name='eliminar_reserva'),

    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),


    path('consultar-disponibilidad/', views.consultar_disponibilidad, name='consultar_disponibilidad'),
    path('api/consultar-disponibilidad/', views.consultar_disponibilidad_api, name='consultar_disponibilidad_api'),

]

