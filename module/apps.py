from django.apps import AppConfig

# clase de configuracion
# de la app module
class ModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'module'
