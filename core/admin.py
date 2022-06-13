from django.contrib import admin
from .models import Funcao, Exame, TipoExame, Risco, TipoRisco, Grupo, Setor
# Register your models here.

admin.site.register(Funcao)
admin.site.register(Exame)
admin.site.register(TipoExame)
admin.site.register(Risco)
admin.site.register(TipoRisco)
admin.site.register(Grupo)
admin.site.register(Setor)


