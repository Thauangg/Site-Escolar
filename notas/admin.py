from django.contrib import admin
from .models import Aluno, Notas, Professor

admin.site.register(Aluno)
admin.site.register(Notas)
admin.site.register(Professor)
