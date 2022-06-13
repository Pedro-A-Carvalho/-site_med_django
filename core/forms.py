from django.forms import ModelForm
from .models import Funcao, Exame, Risco, TipoRisco, Setor, Grupo, TipoExame, GrupoExame, GrupoFuncao, GrupoRisco
from .models import Coordenador, Empregado, Atendimento, AtendimentoRisco, AtendimentoExame

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User


class TrocaSenhaForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']


class FuncaoForm(ModelForm):
    class Meta:
        model = Funcao
        fields = '__all__'


class ExameForm(ModelForm):
    class Meta:
        model = Exame
        fields = '__all__'


class RiscoForm(ModelForm):
    class Meta:
        model = Risco
        fields = '__all__'


class TipoRiscoForm(ModelForm):
    class Meta:
        model = TipoRisco
        fields = '__all__'


class SetorForm(ModelForm):
    class Meta:
        model = Setor
        fields = '__all__'


class GrupoForm(ModelForm):
    class Meta:
        model = Grupo
        fields = '__all__'


class TipoExameForm(ModelForm):
    class Meta:
        model = TipoExame
        fields = '__all__'


class GrupoExameForm(ModelForm):
    class Meta:
        model = GrupoExame
        fields = '__all__'


class GrupoFuncaoForm(ModelForm):
    class Meta:
        model = GrupoFuncao
        fields = '__all__'


class GrupoRiscoForm(ModelForm):
    class Meta:
        model = GrupoRisco
        fields = '__all__'


class CoordenadorForm(ModelForm):
    class Meta:
        model = Coordenador
        fields = '__all__'


class EmpregadoForm(ModelForm):
    class Meta:
        model = Empregado
        fields = '__all__'


class AtendimentoForm(ModelForm):
    class Meta:
        model = Atendimento
        fields = '__all__'


class AtendimentoRiscoForm(ModelForm):
    class Meta:
        model = AtendimentoRisco
        fields = '__all__'


class AtendimentoExameForm(ModelForm):
    class Meta:
        model = AtendimentoExame
        fields = '__all__'



