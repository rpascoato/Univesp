from django.contrib import admin
from .models import Usuario, Perquest, Resposta, Escola, Questionario, Resultado

class RespostaInline(admin.StackedInline):
    model = Resposta
    extra = 1

@admin.register(Perquest)
class PerguntaAdmin(admin.ModelAdmin):
    inlines = [RespostaInline]

admin.site.register(Usuario)
admin.site.register(Escola)
admin.site.register(Questionario)
admin.site.register(Resultado)