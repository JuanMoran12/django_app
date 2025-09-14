from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg
from cuestionario.models import Carreras, Preguntas, Porcentaje, Auditoria
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.cache import cache
from datetime import datetime

def loginn(request):
    print("este es el request imprimido: ", request)
    url_status = "https://http.dog/404.jpg"

    if request.method == "POST":
        usuario = request.POST.get("Usuario")  
        clave = request.POST.get("Clave")  

        print("Usuario recibido:", usuario)
        print("Clave recibida:", clave)

        user = authenticate(username=usuario, password=clave)  
        print("esto es user: ", user)

        if user is not None:
            login(request, user) 
            return redirect("home/")  
        
        else:
            return render(request, "login.html", {"error": "necesita iniciar sesion"})

    return render(request, 'login.html')
    
@login_required(login_url="/")
def primer_view(request):

    all_audits = Auditoria.objects.all()
    
    total_checklists = all_audits.count()
    failed_checklists = all_audits.filter(porcentaje__lt=50).count()
    average_percentage = all_audits.aggregate(avg=Avg('porcentaje'))['avg'] or 0
    average_percentage = round(average_percentage, 2) 
    
    context = {
        'total_checklists': total_checklists,
        'failed_checklists': failed_checklists,
        'average_percentage': average_percentage,
    }
    
    return render(request, "home.html", context)

def cerrar_sesion(request):
    logout(request)
    return redirect("/")  

@login_required(login_url="/")
def tercer_view(request):
    from django.db import transaction
    from django.utils import timezone
    from django.shortcuts import get_object_or_404
    from django.contrib.auth.decorators import login_required
    from django.contrib.auth import logout
    
    consulta1 = Preguntas.objects.filter(id_carrera__id=2)
    carrera = get_object_or_404(Carreras, id=2)
    
    if request.method == "POST":
        try:
            with transaction.atomic():
                respuestas = []
                ids = []
                si = []
                no = []
                
                for pregunta in consulta1:
                    respuesta_key = f"respuesta_{pregunta.id}"
                    id_key = f"escondido_{pregunta.id}"
                    
                    respuesta = request.POST.get(respuesta_key)
                    id_respuesta = request.POST.get(id_key)
                    
                    if respuesta is not None and id_respuesta is not None:
                        respuesta = int(respuesta)
                        respuestas.append(respuesta)
                        ids.append(int(id_respuesta))
                        
                        if respuesta == 1:
                            si.append(respuesta)
                        else:
                            no.append(respuesta)
                
                respuestas_si = len(si)
                respuestas_no = len(no)
                total_respuestas = respuestas_si + respuestas_no
                porcentaje = round((respuestas_si / total_respuestas) * 100) if total_respuestas > 0 else 0
                
                if porcentaje >= 80:
                    color = "#2ecc71"  
                elif porcentaje >= 50:
                    color = "#f1c40f"  
                else:
                    color = "#e74c3c"  
                
                Auditoria.objects.create(
                    fecha=timezone.now().date(),
                    carrera=carrera,
                    porcentaje=porcentaje
                )
                
                if porcentaje >= 80:
                    recomendaciones = [
                        "Excelente trabajo. Se recomienda mantener los estándares actuales.",
                        "Considere documentar las buenas prácticas implementadas.",
                        "Realice capacitaciones periódicas para mantener el nivel de conocimiento.",
                        "Mantenga un programa de mantenimiento preventivo regular."
                    ]
                elif porcentaje >= 50:
                    recomendaciones = [
                        "Se recomienda mejorar en las áreas con menor puntuación.",
                        "Implemente un plan de acción para las áreas críticas.",
                        "Considere capacitación adicional para el personal.",
                        "Realice auditorías más frecuentes para monitorear el progreso."
                    ]
                else:
                    recomendaciones = [
                        "Se requiere atención inmediata en las áreas críticas.",
                        "Implemente un plan de acción correctivo urgente.",
                        "Considere asistencia técnica especializada.",
                        "Realice auditorías semanales para monitorear mejoras."
                    ]
                
                context = {
                    'porcentaje': porcentaje,
                    'si': respuestas_si,
                    'no': respuestas_no,
                    'color': color,
                    'carrera': carrera.nombre,
                    'fecha': timezone.now().date(),
                    'recomendaciones': recomendaciones
                }
                
                return render(request, "resultado.html", context)
                
        except Exception as e:
            print(f"Error processing form: {str(e)}")
            return render(request, "error.html", {"mensaje": "Error al procesar el formulario. Por favor intente nuevamente."})
    
    return render(request, "checklist.html", {
        "resultado": consulta1,
    })

def informatica(request):
    from django.urls import reverse
    from django.utils import timezone
    from django.db import transaction
    
    dict_carreras = {
        "General": reverse('questioner'),
        "Informatica": reverse('informatica'),
        "Diseño Grafico": reverse('grafico')
    }
    
    consulta2 = Preguntas.objects.filter(id_carrera_id=1)
    carreras = Carreras.objects.all()
    carrera = Carreras.objects.get(id=1)
    
    if request.method == "POST":
        with transaction.atomic():
            respuestas = []
            si = []
            no = []
            
            computadoras_evaluadas = int(request.POST.get('computadoras_evaluadas', 1))
            computadoras_aprobadas = int(request.POST.get('computadoras_aprobadas', 0))
            
            fecha = timezone.now().date()
            for i in consulta2:
                respuesta_sino = f"respuesta_{i.id}"
                respuesta = request.POST.get(respuesta_sino)
                
                if respuesta is not None:
                    respuesta = int(respuesta)
                    respuestas.append(respuesta)
                    
                    if respuesta == 1:
                        si.append(respuesta)
                    else:
                        no.append(respuesta)
            
            respuestas_si = len(si)
            respuesta_no = len(no)
            total_preguntas = len(respuestas)
            porcentaje = (respuestas_si / total_preguntas) * 100 if total_preguntas > 0 else 0
            porcentaje = round(porcentaje, 2)
            
            Porcentaje.objects.create(
                fecha=fecha,
                carrera=carrera,
                equipos_aprobados=computadoras_aprobadas,
                equipos_evaluados=computadoras_evaluadas,
                equipos_reprobados=computadoras_evaluadas - computadoras_aprobadas,
                indice_aprobacion=porcentaje
            )
            
            if 50 <= porcentaje <= 70:
                color = "#ccc92e"  
            elif porcentaje > 90:
                color = "#2ecc71"   
            else:
                color = "#cc2e2e"   

            return render(request, "res_cues.html", {
                "resultado": respuestas,
                "si": respuestas_si,
                "no": respuesta_no,
                "porcentaje": porcentaje,
                "color": color,
                "carrera": carrera.nombre if carrera else "Informática",
                "fecha": fecha,
                "computadoras_evaluadas": computadoras_evaluadas,
                "computadoras_aprobadas": computadoras_aprobadas
            })

    return render(request, "cues.html", {
        "cues": consulta2,
        "carreras": dict_carreras,
        "carrera_actual": "Informatica",
        "todas_carreras": carreras
    })

def grafico(request):
    from django.urls import reverse
    from django.utils import timezone
    from django.db import transaction
    
    dict_carreras = {
        "General": reverse('questioner'),
        "Informatica": reverse('informatica'),
        "Diseño Grafico": reverse('grafico')
    }
    
    consulta3 = Preguntas.objects.filter(id_carrera_id=4)
    carreras = Carreras.objects.all()
    
    if request.method == "POST":
        with transaction.atomic():
            respuestas = []
            si = []
            no = []
            
            carrera_id = request.POST.get('carrera')
            carrera = get_object_or_404(Carreras, id=carrera_id) if carrera_id else None
            
            computadoras_evaluadas = int(request.POST.get('computadoras_evaluadas', 1))
            computadoras_aprobadas = int(request.POST.get('computadoras_aprobadas', 0))
            
            fecha_evaluacion = request.POST.get('fecha_evaluacion')
            fecha = timezone.datetime.strptime(fecha_evaluacion, '%Y-%m-%d').date() if fecha_evaluacion else timezone.now().date()
            
            for i in consulta3:
                respuesta_sino = f"respuesta_{i.id}"
                respuesta = request.POST.get(respuesta_sino)
                
                if respuesta is not None:
                    respuesta = int(respuesta)
                    respuestas.append(respuesta)
                    
                    if respuesta == 1:
                        si.append(respuesta)
                    else:
                        no.append(respuesta)
            
            respuestas_si = len(si)
            respuesta_no = len(no)
            total_preguntas = len(respuestas)
            porcentaje = (respuestas_si / total_preguntas) * 100 if total_preguntas > 0 else 0
            porcentaje = round(porcentaje, 2)
            
            Porcentaje.objects.create(
                fecha=fecha,
                carrera=carrera,
                equipos_aprobados=computadoras_aprobadas,
                equipos_evaluados=computadoras_evaluadas,
                equipos_reprobados=computadoras_evaluadas - computadoras_aprobadas,
                indice_aprobacion=porcentaje
            )
            
            if 50 <= porcentaje <= 70:
                color = "#ccc92e"  
            elif porcentaje > 90:
                color = "#2ecc71"   
            else:
                color = "#cc2e2e"   

            return render(request, "res_cues.html", {
                "resultado": respuestas,
                "si": respuestas_si,
                "no": respuesta_no,
                "porcentaje": porcentaje,
                "color": color,
                "carrera": carrera.nombre if carrera else "Diseño Gráfico",
                "fecha": fecha,
                "computadoras_evaluadas": computadoras_evaluadas,
                "computadoras_aprobadas": computadoras_aprobadas
            })

    #return render(request, "cues.html", {"consulta" : consulta3})
    return render(request, "cues.html", {
        "cues": consulta3,
        "carreras": dict_carreras,
        "carrera_actual": "Diseño Grafico"
    })

def cuestionario_solo(request):
    from django.urls import reverse
    from django.db import transaction
    
    dict_carreras = {
        "General": reverse('questioner'),
        "Informatica": reverse('informatica'),
        "Diseño Grafico": reverse('grafico')
    }
    
    consulta_cues = Preguntas.objects.filter(id_carrera_id=5)
    carreras = Carreras.objects.all()
    carrera = Carreras.objects.get(id=5)
    
    if request.method == "POST":
        with transaction.atomic():
            respuestas = []
            ids = []
            si = []
            no = []
            
            computadoras_evaluadas = int(request.POST.get('computadoras_evaluadas', 1))
            computadoras_aprobadas = int(request.POST.get('computadoras_aprobadas', 0))

            fecha = datetime.now().date()

            for i in consulta_cues:
                respuesta_sino = f"respuesta_{i.id}"
                respuesta = request.POST.get(respuesta_sino)

                if respuesta is not None:
                    respuesta = int(respuesta)
                    respuestas.append(int(respuesta))  
                    ids.append(i.id)

                    if respuesta == 1:
                        si.append(respuesta)  
                    else:
                        no.append(respuesta) 

            respuestas_si = len(si)
            respuesta_no = len(no)
            total_preguntas = consulta_cues.count()
            porcentaje = (respuestas_si / total_preguntas) * 100 if total_preguntas > 0 else 0
            porcentaje = round(porcentaje, 2)
            
            Porcentaje.objects.create(
                fecha=fecha,
                carrera=carrera,
                equipos_aprobados=computadoras_aprobadas,
                equipos_evaluados=computadoras_evaluadas,
                equipos_reprobados=computadoras_evaluadas - computadoras_aprobadas,
                indice_aprobacion=porcentaje
            )
        
        color = ""
        if 50 <= porcentaje <= 70:
            color = '#ccc92e'  
        elif porcentaje >= 80:
            color = '#2ecc71'       
        elif porcentaje <= 40:
            color = '#cc2e2e' 

        return render(request, "res_cues.html", {
            "resultado": respuestas, 
            "si": respuestas_si, 
            "no": respuesta_no, 
            "porcentaje": porcentaje, 
            "color": color,
            "carrera": carrera.nombre if carrera else "General"
        })

    return render(request, "cues.html", {
        "cues": consulta_cues,
        "carreras": dict_carreras,
        "carrera_actual": "General",
        "todas_carreras": carreras,
    })

def mostrar_informe(request):
    if request.method == "GET":

        fecha = request.GET.get("fecha") or None
        carrera_nombre = request.GET.get("carrera") or None
        estado = request.GET.get("estado") or None

        print("fecha digitada: ", fecha, "carrera digitada: ", carrera_nombre, "estado digitado: ", estado)

        # Build queryset incrementally based on provided filters
        qs = Porcentaje.objects.all()

        if fecha:
            qs = qs.filter(fecha=fecha)
        if carrera_nombre:
            qs = qs.filter(carrera__nombre__icontains=carrera_nombre)
        if estado:
            estado = estado.lower()
            if estado == "alto":
                qs = qs.filter(indice_aprobacion__gte=80)
            elif estado == "medio":
                qs = qs.filter(indice_aprobacion__gte=50, indice_aprobacion__lt=80)
            elif estado == "bajo":
                qs = qs.filter(indice_aprobacion__lt=50)

        porcentajes = qs.order_by("-fecha")
        
        data = []
        for p in porcentajes:
            data.append({
                'fecha': p.fecha.strftime('%Y-%m-%d'),
                'carrera': p.carrera.nombre if p.carrera else 'Sin carrera',
                'indice_aprobacion': float(p.indice_aprobacion),
                'equipos_evaluados': p.equipos_evaluados,
                'equipos_aprobados': p.equipos_aprobados,
                'equipos_reprobados': p.equipos_reprobados,
            })
        
        return JsonResponse({"porcentajes": data})

def informes(request):

    lista_porcentaje = []

    resultados = Porcentaje.objects.all()
    for i in resultados:
        print("Tabla Porcentaje: ",i.fecha, i.indice_aprobacion, i.carrera)

        fecha_por = str(i.fecha)
        porcentaje_por = str(i.indice_aprobacion)
        carrera_por = str(i.carrera)

        print("texto formateado a cadena: ",fecha_por, porcentaje_por, carrera_por)

        tupla_porcentaje = (fecha_por, porcentaje_por, carrera_por)
        lista_porcentaje.append(tupla_porcentaje)

    mensaje_error = ""

    if request.method == "POST":
        
        salida = request.POST.get("consulta")

        consulta_id = Carreras.objects.filter(nombre=salida).first()
        print(consulta_id)

        lista = []

        if consulta_id is not None:
            porcentajes = Porcentaje.objects.filter(carrera=consulta_id)
            for i in porcentajes:
                print(f"{i.fecha} {i.indice_aprobacion} {i.carrera}")

                fecha_barra = str(i.fecha)
                porce_barra = str(i.indice_aprobacion)
                carrara_barra = str(i.carrera)

                tupla = (fecha_barra, porce_barra, carrara_barra)
                lista.append(tupla)

            print(lista)
        else:
            mensaje_error = "No existe esa carrera"

        return render(request, "informes.html", {"consulta" : consulta_id, "porcentajes_generales" : lista_porcentaje, "lista_de_tupla" : lista[-5:], "error" : mensaje_error})

    return render(request, "informes.html", {"porcentajes_generales" : lista_porcentaje[-5:]})
