from django.db import models, reset_queries
from django.contrib.auth.models import User

#3rd apps field
from ckeditor.fields import RichTextField

import os

# Create your models here.

# Esta función retorna la ruta 
# de almacenamiento 
# de archivos de un usuario
def user_directory_path(instance, filename):
	#THis file will be uploaded to MEDIA_ROOT /the user_(id)/the file
	return 'user_{0}/{1}'.format(instance.user.id, filename)

# Esta clase define la estructura 
# en la base de datos
# de los objetos Contenido de tarea
class AssignmentFileContent(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	file = models.FileField(upload_to=user_directory_path)

	def get_file_name(self):
		return os.path.basename(self.file.name)

# Esta clase define la estructura 
# en la base de datos
# de los objetos Tarea
class Assignment(models.Model):
	title = models.CharField(max_length=150)
	content = RichTextField()
	points = models.PositiveIntegerField()
	due = models.DateField()
	files = models.ManyToManyField(AssignmentFileContent)

	def __str__(self):
		return self.title

# Esta clase define la estructura 
# en la base de datos
# de los objetos Respuesta de tarea
class Submission(models.Model):
	file = models.FileField(upload_to=user_directory_path)
	points = models.PositiveIntegerField(default=0)
	delivered = models.BooleanField(default=False)
	onTime = models.BooleanField(default=False)
	checked = models.BooleanField(default=False)
	date = models.DateTimeField(null=True)
	assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def get_file_name(self):
		return os.path.basename(self.file.name)
