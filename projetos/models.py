from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Escola(models.Model):
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)

    #def __str__(self):
        #return str(self.id) 

    def __str__(self):
        return self.nome
   

class Perquest(models.Model):
    texto = models.TextField()

    def __str__(self):
        return self.texto

class Resposta(models.Model):
    pergunta = models.ForeignKey(Perquest, on_delete=models.CASCADE)
    texto = models.TextField()
    valor = models.IntegerField()

    def __str__(self):
        return self.texto
    
class Questionario(models.Model):
    nome = models.CharField(max_length=100) 
    idade = models.IntegerField(default = 0)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    

class Usuario(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Resultado(models.Model):
    ESPECTRO_CHOICES = [
        ('Alto', 'Alto'),
        ('Médio', 'Médio'),
        ('Baixo', 'Baixo'),
    ]

    nivel = models.CharField(max_length=10, choices=ESPECTRO_CHOICES)
    cod_ques = models.ForeignKey(Questionario, on_delete=models.CASCADE)
    cod_usu = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nivel