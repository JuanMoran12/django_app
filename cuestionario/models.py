from django.db import models

class Carreras(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Preguntas(models.Model):
    pregunta = models.CharField(max_length=200)
    id_carrera = models.ForeignKey(Carreras, on_delete=models.CASCADE)

    def __str__(self):
        return self.pregunta

""" class Equipo(models.Model):
        nombre = models.CharField(max_length=100)  
        modelo = models.CharField(max_length=100)   

        def __str__(self):
            return f"{self.nombre} - {self.modelo}"""

class Porcentaje(models.Model):
    fecha = models.DateField(auto_now_add=True)
    carrera = models.ForeignKey("Carreras", on_delete=models.CASCADE)
    equipos_evaluados = models.IntegerField(default=0)
    equipos_aprobados = models.IntegerField(default=0)
    equipos_reprobados = models.IntegerField(default=0)
    indice_aprobacion = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        if self.equipos_reprobados == 0:
            self.equipos_reprobados = self.equipos_evaluados - self.equipos_aprobados

        if self.equipos_evaluados > 0:
            self.indice_aprobacion = (self.equipos_aprobados / self.equipos_evaluados) * 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.carrera.nombre} - {self.indice_aprobacion:.2f}% ({self.fecha})"

class Auditoria(models.Model):
    fecha = models.DateField(auto_now_add=True)
    carrera = models.ForeignKey("Carreras", on_delete=models.CASCADE)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.carrera.nombre} - {self.porcentaje:.2f}% ({self.fecha})" 

"""class EvaluacionEquipo(models.Model):
    equipo = models.ForeignKey("Equipo", on_delete=models.CASCADE)
    auditoria = models.ForeignKey("Porcentaje", on_delete=models.CASCADE)
    cumple = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.equipo.nombre} - {'Cumple' if self.cumple else 'No cumple'}"""

    
# tabla para el porcentaje
"""class Porcentaje(models.Model):
    fecha = models.DateField(auto_now_add=True)
    porcentaje = models.IntegerField()
    carrera = models.ForeignKey(Carreras, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.porcentaje, self.fecha)"""