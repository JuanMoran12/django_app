from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.loginn, name='login'),
    path("home/", views.primer_view, name='home'),
    path("checklist/", views.tercer_view, name='checklist'),
    path("questioner/", views.cuestionario_solo, name='questioner'),
    path("informatica/", views.informatica, name='informatica'),
    path("grafico/", views.grafico, name='grafico'),
    path("cerrar/", views.cerrar_sesion, name='cerrar_sesion'),
    path("informes/", views.informes, name='informes'),
    path("mostrar_informe/", views.mostrar_informe, name='mostrar_informe')
]
