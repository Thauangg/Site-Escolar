from django.db import models
from django.contrib.auth.models import AbstractUser

class Professor(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username  # ou use self.nome se você adicionar um campo nome

class Aluno(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Notas(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    semestre = models.IntegerField()
    nota1 = models.DecimalField(max_digits=5, decimal_places=2)
    nota2 = models.DecimalField(max_digits=5, decimal_places=2)
    nota3 = models.DecimalField(max_digits=5, decimal_places=2)

    def media_semestre(self):
        return (self.nota1 + self.nota2 + self.nota3) / 3

    def status(self):
        return "Aprovado" if self.media_semestre() >= 7 else "Reprovado"

    def __str__(self):
        return f'Notas de {self.aluno.nome} - Semestre {self.semestre}'