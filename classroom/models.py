from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid

# Create your models here.
from module.models import Module
from assignment.models import Submission
from question.models import Question

# 3rd apps field
from ckeditor.fields import RichTextField

STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('graded', 'Graded'),
)

# Esta función retorna la 
# ruta de almacenamiento 
# de archivos de un usuario
def user_directory_path(instance, filename):
    # THis file will be uploaded to MEDIA_ROOT /the user_(id)/the file
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# Esta clase define la estructura 
# en la base de datos
# de los objetos Categoría de un curso
class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    icon = models.CharField(max_length=100, verbose_name='Icon', default='article')
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('categories', arg=[self.slug])

    def __str__(self):
        return self.title

# Esta clase define la 
# estructura en la base de datos
# de los objetos Curso
class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to=user_directory_path)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    DAY_CHOICES = [
        ('1', 'Lunes'),
        ('2', 'Martes'),
        ('3', 'Miércoles'),
        ('4', 'Jueves'),
        ('5', 'Viernes'),
        ('6', 'Sábado'),
        ('7', 'Domingo')
    ]
    day = models.CharField(
        max_length=1,
        choices=DAY_CHOICES,
        default='1'
    )
    time_start = models.TimeField()
    time_end = models.TimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    syllabus = RichTextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_owner')
    enrolled = models.ManyToManyField(User)
    modules = models.ManyToManyField(Module)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.title

# Esta clase define la 
# estructura en la base de datos
# de los objetos Nota
class Grade(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    grade = models.PositiveIntegerField(default=0)
