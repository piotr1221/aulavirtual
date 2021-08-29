from django.db import models
from django.contrib.auth.models import User

from page.models import Page
from quiz.models import Quizzes
from assignment.models import Assignment

# Create your models here.
#Funcion Prueba
#Texto Prueba
# Esta clase define la estructura 
# en la base de datos
# de los objetos Categoría de un curso
class Module(models.Model):
	title = models.CharField(max_length=150)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_owner')
	hours = models.PositiveIntegerField()
	pages = models.ManyToManyField(Page)
	quizzes = models.ManyToManyField(Quizzes)
	assignments = models.ManyToManyField(Assignment)

	def __str__(self):
		return self.title