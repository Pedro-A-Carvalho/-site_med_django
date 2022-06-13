import io

from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from .models import Funcao, Setor, TipoRisco, Risco, Exame, Grupo, Empregado, GrupoFuncao, GrupoRisco, GrupoExame
from .models import TipoExame, Coordenador, Atendimento, AtendimentoRisco, AtendimentoExame
from .forms import FuncaoForm, SetorForm, TipoRiscoForm, RiscoForm, ExameForm, GrupoForm, EmpregadoForm, \
    GrupoFuncaoForm, GrupoRiscoForm, GrupoExameForm
from .forms import TipoExameForm, CoordenadorForm, AtendimentoForm, AtendimentoRiscoForm, AtendimentoExameForm
from .forms import TrocaSenhaForm
from django.contrib.auth.decorators import login_required
from report.report import report

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView

# import xhtml2pdf as pisa
# import io
# from django.template.loader import get_template

from django.contrib.auth import update_session_auth_hash


# Create your views here.
@login_required
def alterar_senha(request):
    if request.method == 'POST':
        form = TrocaSenhaForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "senha alterada com sucesso")
            return redirect('alterar_senha')
        else:
            messages.success(request, 'Informe corretamente a senha anterior')
            return redirect('alterar_senha')
    else:
        form = TrocaSenhaForm(user=request.user)
        return render(request, 'alterar_senha.html', {'form': form})


@login_required
def home(request):
    return render(request, 'home.html')


# Comeco funcoes
@login_required
def lista_funcoes(request):
    form = FuncaoForm
    funcoes_list = Funcao.objects.all().order_by('nome')
    paginator = Paginator(funcoes_list, 10)
    page = request.GET.get('page')
    funcoes = paginator.get_page(page)
    return render(request, 'lista_funcoes.html', {'form': form, 'funcoes': funcoes})


# @login_required
class ListaFuncoes(ListView):
    queryset = Funcao.objects.all().order_by(
        'pk')  # model = Funcao  # queryset = Funcao.objects.  pode ser usado para filtrar ou pegar todos
    context_object_name = 'funcoes'
    paginate_by = 5

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@login_required
def funcao_novo(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        count = Funcao.objects.filter(nome=nome).count()
        if count > 0:
            messages.error(request, 'Registro ja cadastrado com este Nome')
            return redirect('funcao_novo')
        else:
            form = FuncaoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("lista_funcoes")
    else:
        form = FuncaoForm
        return render(request, 'funcao_novo.html', {'form': form})


class FuncaoNovo(CreateView):
    model = Funcao
    fields = ['nome']
    template_name = 'core/funcao_novo2.html'
    success_url = reverse_lazy('lista_funcoes')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@login_required
def funcao_update(request, pk):
    funcao = Funcao.objects.get(pk=pk)
    form = FuncaoForm(request.POST or None, instance=funcao)
    data = {
        'funcao': funcao,
        'form': form,
    }
    if request.method == 'POST':
        nome = request.POST.get('nome')
        count = Funcao.objects.filter(nome=nome).exclude(pk=pk).count()
        if count > 0:
            messages.error(request, 'Registro ja cadastrado com este Nome')
            return redirect('funcao_update', pk)
        if form.is_valid():
            form.save()
            return redirect("lista_funcoes")
    else:
        return render(request, 'funcao_update.html', data)


class FuncaoUpdate(UpdateView):
    model = Funcao
    fields = ['nome']
    template_name = 'core/funcao_update.html'
    success_url = reverse_lazy('lista_funcoes')
    context_object_name = 'funcao'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@login_required
def funcao_search(request):
    search = request.GET.get('search')
    funcoes = Funcao.objects.filter(nome__icontains=search)
    form = FuncaoForm()
    data = {
        'funcoes': funcoes,
        'form': form,
    }
    return render(request, "lista_funcoes.html", data)


@login_required
def funcao_delete(request, pk):
    funcao = Funcao.objects.get(pk=pk)
    funcao.delete()
    messages.success(request, 'Registro Excluido com sucesso')
    return redirect('lista_funcoes')


# Comeco setores
@login_required
def lista_setores(request):
    form = SetorForm
    setores_list = Setor.objects.all().order_by('nome')
    paginator = Paginator(setores_list, 10)
    page = request.GET.get('page')
    setores = paginator.get_page(page)
    return render(request, 'lista_setores.html', {'form': form, 'setores': setores})


@login_required
def setor_novo(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        count = Setor.objects.filter(nome=nome).count()
        if count > 0:
            messages.error(request, 'Registro ja cadastrado com este Nome')
            return redirect('setor_novo')
        else:
            form = SetorForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("lista_setores")
    else:
        form = SetorForm
        return render(request, 'setor_novo.html', {'form': form})


@login_required
def setor_update(request, pk):
    setor = Setor.objects.get(pk=pk)
    form = SetorForm(request.POST or None, instance=setor)
    data = {
        'setor': setor,
        'form': form,
    }
    if request.method == 'POST':
        nome = request.POST.get('nome')
        count = Setor.objects.filter(nome=nome).exclude(pk=pk).count()
        if count > 0:
            messages.error(request, 'Registro ja cadastrado com este Nome')
            return redirect('setor_update', pk)
        if form.is_valid():
            form.save()
            return redirect("lista_setores")
    else:
        return render(request, 'setor_update.html', data)


@login_required
def setor_search(request):
    search = request.GET.get('search')
    setores = Setor.objects.filter(nome__icontains=search)
    form = SetorForm()
    data = {
        'setores': setores,
        'form': form,
    }
    return render(request, "lista_setores.html", data)


@login_required
def setor_delete(request, pk):
    setor = Setor.objects.get(pk=pk)
    setor.delete()
    messages.success(request, 'Registro Excluido com sucesso')
    return redirect('lista_setores')


# Tipo riscos
@login_required
def lista_tipo_riscos(request):
    form = TipoRiscoForm
    tipo_riscos = TipoRisco.objects.all().order_by('nome')
    return render(request, 'lista_tipo_riscos.html', {'form': form, 'tipo_riscos': tipo_riscos})


@login_required
def tipo_risco_novo(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        count = TipoRisco.objects.filter(nome=nome).count()
        if count > 0:
            messages.error(request, 'Registro ja cadastrado com este Nome')
            return redirect('tipo_risco_novo')
        else:
            form = TipoRiscoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("lista_tipo_riscos")
    else:
        form = TipoRiscoForm
        return render(request, 'tipo_risco_novo.html', {'form': form})


@login_required
def tipo_risco_update(request, pk):
    tipo_risco = TipoRisco.objects.get(pk=pk)
    form = TipoRiscoForm(request.POST or None, instance=tipo_risco)
    data = {
        'tipo_risco': tipo_risco,
        'form': form,
    }
    if request.method == 'POST':
        nome = request.POST.get('nome')
        count = TipoRisco.objects.filter(nome=nome).exclude(pk=pk).count()
        if count > 0:
            messages.error(request, 'Registro ja cadastrado com este Nome')
            return redirect('tipo_risco_update', pk)
        if form.is_valid():
            form.save()
            return redirect("lista_tipo_riscos")
    else:
        return render(request, 'tipo_risco_update.html', data)


@login_required
def tipo_risco_delete(request, pk):
    tipo_risco = TipoRisco.objects.get(pk=pk)
    tipo_risco.delete()
    messages.success(request, 'Registro Excluido com sucesso')
    return redirect('lista_tipo_riscos')


# Comeco riscos keywords riscos risco Risco
@login_required
def lista_riscos(request):
    form = RiscoForm
    riscos_list = Risco.objects.all().order_by('nome')
    paginator = Paginator(riscos_list, 10)
    page = request.GET.get('page')
    riscos = paginator.get_page(page)
    data = {
        'riscos': riscos,
        'form': form
    }
    return render(request, 'lista_riscos.html', data)


@login_required
def risco_novo(request):
    if request.method == 'POST':
        nome = request.POST.get('id_nome')
        # tiporisco_id = request.POST.get('id_tiporisco')
        count = Risco.objects.filter(nome=nome).count()
        if count > 0:
            messages.error(request, 'Registro ja cadastrado com este Nome')
            return redirect('risco_novo')
        else:
            form = RiscoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("lista_riscos")
    else:
        form = RiscoForm
        tiporiscos = TipoRisco.objects.all()
        data = {
            'form': form,
            'tiporiscos': tiporiscos
        }
        return render(request, 'risco_novo.html', data)


@login_required
def risco_update(request, pk):
    risco = Risco.objects.get(pk=pk)
    form = RiscoForm(request.POST or None, instance=risco)
    tiporiscos = TipoRisco.objects.all()
    data = {
        'tiporiscos': tiporiscos,
        'risco': risco,
        'form': form,
    }
    if request.method == 'POST':
        nome = request.POST.get('nome')
        count = Risco.objects.filter(nome=nome).exclude(pk=pk).count()
        if count > 0:
            messages.error(request, 'Registro ja cadastrado com este Nome')
            return redirect('risco_update', pk)
        if form.is_valid():
            form.save()
            return redirect("lista_riscos")
    else:
        return render(request, 'risco_update.html', data)


@login_required
def risco_search(request):
    search = request.GET.get('search')
    riscos = Risco.objects.filter(nome__icontains=search)
    form = RiscoForm()
    data = {
        'riscos': riscos,
        'form': form,
    }
    return render(request, "lista_riscos.html", data)


@login_required
def risco_delete(request, pk):
    risco = Risco.objects.get(pk=pk)
    risco.delete()
    messages.success(request, 'Registro Excluido com sucesso')
    return redirect('lista_riscos')


# Comeco exames keyword Exame exames exame
@login_required
def lista_exames(request):
    form = ExameForm
    exames_list = Exame.objects.all().order_by('nome')
    paginator = Paginator(exames_list, 10)
    page = request.GET.get('page')
    exames = paginator.get_page(page)
    return render(request, 'lista_exames.html', {'form': form, 'exames': exames})


@login_required
def exame_novo(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        count = Exame.objects.filter(nome=nome).count()
        if count > 0:
            messages.error(request, 'Registro ja cadastrado com este Nome')
            return redirect('exame_novo')
        else:
            form = ExameForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("lista_exames")
    else:
        form = ExameForm
        return render(request, 'exame_novo.html', {'form': form})


@login_required
def exame_update(request, pk):
    exame = Exame.objects.get(pk=pk)
    form = ExameForm(request.POST or None, instance=exame)
    data = {
        'exame': exame,
        'form': form,
    }
    if request.method == 'POST':
        nome = request.POST.get('nome')
        count = Exame.objects.filter(nome=nome).exclude(pk=pk).count()
        if count > 0:
            messages.error(request, 'Registro ja cadastrado com este Nome')
            return redirect('exame_update', pk)
        if form.is_valid():
            form.save()
            return redirect("lista_exames")
    else:
        return render(request, 'exame_update.html', data)


@login_required
def exame_search(request):
    search = request.GET.get('search')
    exames = Exame.objects.filter(nome__icontains=search)
    form = ExameForm()
    data = {
        'exames': exames,
        'form': form,
    }
    return render(request, "lista_exames.html", data)


@login_required
def exame_delete(request, pk):
    exame = Exame.objects.get(pk=pk)
    exame.delete()
    messages.success(request, 'Registro Excluido com sucesso')
    return redirect('lista_exames')


# Tipo riscos keywords Grupo grupos grupo
@login_required
def lista_grupos(request):
    form = GrupoForm
    grupos = Grupo.objects.all().order_by('nome')
    return render(request, 'lista_grupos.html', {'form': form, 'grupos': grupos})


@login_required
def grupo_novo(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        count = Grupo.objects.filter(nome=nome).count()
        if count > 0:
            messages.error(request, 'Registro ja cadastrado com este Nome')
            return redirect('grupo_novo')
        else:
            form = GrupoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("lista_grupos")
    else:
        form = GrupoForm
        return render(request, 'grupo_novo.html', {'form': form})


@login_required
def grupo_update(request, pk):
    grupo = Grupo.objects.get(pk=pk)
    form = GrupoForm(request.POST or None, instance=grupo)
    data = {
        'grupo': grupo,
        'form': form,
    }
    if request.method == 'POST':
        nome = request.POST.get('nome')
        count = Grupo.objects.filter(nome=nome).exclude(pk=pk).count()
        if count > 0:
            messages.error(request, 'Registro ja cadastrado com este Nome')
            return redirect('grupo_update', pk)
        if form.is_valid():
            form.save()
            return redirect("lista_grupos")
    else:
        return render(request, 'grupo_update.html', data)


@login_required
def grupo_delete(request, pk):
    grupo = Grupo.objects.get(pk=pk)
    grupo.delete()
    messages.success(request, 'Registro Excluido com sucesso')
    return redirect('lista_grupos')


@login_required
def grupofuncao_novo(request, pk):
    grupo = Grupo.objects.get(pk=pk)
    grupofuncoes = GrupoFuncao.objects.filter(grupo_id=pk)
    setores = Setor.objects.all().order_by('nome')
    funcoes = Funcao.objects.all().order_by('nome')
    data = {
        'grupo': grupo,
        'grupofuncoes': grupofuncoes,
        'setores': setores,
        'funcoes': funcoes,
    }
    if request.method == 'POST':
        funcao_id = request.POST.get('funcao_id')
        setor_id = request.POST.get('setor_id')
        count = GrupoFuncao.objects.filter(grupo_id=pk, funcao_id=funcao_id, setor_id=setor_id).count()
        if count > 0:
            messages.error(request, "Registro ja cadastrado !")
            return redirect('/grupofuncao_novo/' + str(pk))
        else:
            g = GrupoFuncao.objects.create(
                grupo_id=pk,
                funcao_id=funcao_id,
                setor_id=setor_id
            )
            return redirect('/grupofuncao_novo/' + str(pk))
    else:
        form = GrupoForm
        return render(request, 'grupofuncao_novo.html', data)


@login_required
def grupofuncao_delete(request, pk):
    grupofuncao = GrupoFuncao.objects.get(pk=pk)
    grupo_id = grupofuncao.grupo_id
    grupofuncao.delete()
    return redirect("/grupofuncao_novo/" + str(grupo_id))


@login_required
def gruporisco_novo(request, pk):
    grupo = Grupo.objects.get(pk=pk)
    gruporiscos = GrupoRisco.objects.filter(grupo_id=pk)
    riscos = Risco.objects.all().order_by('nome')
    data = {
        'grupo': grupo,
        'gruporiscos': gruporiscos,
        'riscos': riscos,
    }
    if request.method == 'POST':
        risco_id = request.POST.get('risco_id')
        count = GrupoRisco.objects.filter(grupo_id=pk, risco_id=risco_id).count()
        if count > 0:
            messages.error(request, "Registro ja cadastrado !")
            return redirect('/gruporisco_novo/' + str(pk))
        else:
            g = GrupoRisco.objects.create(
                grupo_id=pk,
                risco_id=risco_id
            )
            return redirect('/gruporisco_novo/' + str(pk))
    else:
        return render(request, 'gruporisco_novo.html', data)


@login_required
def gruporisco_delete(request, pk):
    gruporisco = GrupoRisco.objects.get(pk=pk)
    grupo_id = gruporisco.grupo_id
    gruporisco.delete()
    return redirect("/gruporisco_novo/" + str(grupo_id))


# tipo
@login_required
def grupoexame_novo(request, pk):
    grupo = Grupo.objects.get(pk=pk)
    grupoexames = GrupoExame.objects.filter(grupo_id=pk)
    exames = Exame.objects.all().order_by('nome')
    tipoexames = TipoExame.objects.all().order_by('nome')
    data = {
        'grupo': grupo,
        'grupoexames': grupoexames,
        'exames': exames,
        'tipoexames': tipoexames,
    }
    if request.method == 'POST':
        exame_id = request.POST.get('exame_id')
        tipoexame_id = request.POST.get('tipoexame_id')
        count = GrupoExame.objects.filter(grupo_id=pk, exame_id=exame_id).count()
        if count > 0:
            messages.error(request, "Registro ja cadastrado !")
            return redirect('/grupoexame_novo/' + str(pk))
        else:
            g = GrupoExame.objects.create(
                grupo_id=pk,
                exame_id=exame_id,
                tipoexame_id=tipoexame_id
            )
            return redirect('/grupoexame_novo/' + str(pk))
    else:
        return render(request, 'grupoexame_novo.html', data)


@login_required
def grupoexame_delete(request, pk):
    grupoexame = GrupoExame.objects.get(pk=pk)
    grupo_id = grupoexame.grupo_id
    grupoexame.delete()
    return redirect("/grupoexame_novo/" + str(grupo_id))


# empregados com class
class ListaEmpregados(ListView):
    model = Empregado
    context_object_name = 'empregados'


class EmpregadoNovo(CreateView):
    model = Empregado
    success_url = reverse_lazy('lista_empregados')
    fields = ['nome', 'cpf', 'ctps', 'serie', 'data_nascimento', 'data_inicio', 'data_fim', 'grupo', 'setor',
              'funcao']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['setores'] = Setor.objects.all().order_by('nome')
        context['funcoes'] = Funcao.objects.all().order_by('nome')
        context['grupos'] = Grupo.objects.all().order_by('nome')
        return context



# comeco empregados kw empregados
@login_required
def lista_empregados(request):
    form = EmpregadoForm
    empregados = Empregado.objects.all().order_by('nome')
    return render(request, 'lista_empregados.html', {'form': form, 'empregados': empregados})


@login_required
def empregado_novo(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        ctps = request.POST.get('ctps')
        serie = request.POST.get('serie')
        data_nascimento = request.POST.get('data_nascimento')
        dia = data_nascimento[0:2]
        mes = data_nascimento[3:5]
        ano = data_nascimento[6:10]
        data_nascimento = str(ano) + '-' + str(mes) + '-' + str(dia)
        data_admissao = request.POST.get('data_admissao')
        dia = data_admissao[0:2]
        mes = data_admissao[3:5]
        ano = data_admissao[6:10]
        data_admissao = str(ano) + '-' + str(mes) + '-' + str(dia)
        data_demissao = request.POST.get('data_demissao')
        grupo_id = request.POST.get('grupo_id')
        setor_id = request.POST.get('setor_id')
        funcao_id = request.POST.get('funcao_id')
        count = Empregado.objects.filter(nome=nome, cpf=cpf).count()
        if count > 0:
            messages.error(request, 'Empregado ja cadastrado com este Nome e CPF')
            return redirect('empregado_novo')
        else:
            if data_demissao == '':
                e = Empregado.objects.create(
                    nome=nome,
                    cpf=cpf,
                    ctps=ctps,
                    serie=serie,
                    data_nascimento=data_nascimento,
                    data_inicio=data_admissao,
                    grupo_id=grupo_id,
                    setor_id=setor_id,
                    funcao_id=funcao_id,
                    data_fim=None
                )
            else:
                dia = data_demissao[0:2]
                mes = data_demissao[3:5]
                ano = data_demissao[6:10]
                data_demissao = str(ano) + '-' + str(mes) + '-' + str(dia)
                e = Empregado.objects.create(
                    nome=nome,
                    cpf=cpf,
                    ctps=ctps,
                    serie=serie,
                    data_nascimento=data_nascimento,
                    data_inicio=data_admissao,
                    grupo_id=grupo_id,
                    setor_id=setor_id,
                    funcao_id=funcao_id,
                    data_fim=data_demissao
                )
            messages.success(request, 'Registro Cadastrado com sucesso')
            return redirect("lista_empregados")
    else:
        form = EmpregadoForm
        setores = Setor.objects.all().order_by('nome')
        funcao = Funcao.objects.all().order_by('nome')
        grupo = Grupo.objects.all().order_by('nome')
        data = {
            'form': form,
            'setores': setores,
            'funcao': funcao,
            'grupo': grupo,
        }
        return render(request, 'empregado_novo.html', data)


@login_required
def load_funcoes(request):
    setor_id = request.GET.get('setor')
    grupos = GrupoFuncao.objects.filter(setor_id=setor_id).all()
    return render(request, 'funcao_ajax.html', {'grupos': grupos})


@login_required
def load_grupos(request):
    setor_id = request.GET.get('setor')
    funcao_id = request.GET.get('funcao')
    grupos = GrupoFuncao.objects.filter(setor_id=setor_id, funcao_id=funcao_id).all()
    return render(request, 'grupo_ajax.html', {'grupos': grupos})


@login_required
def empregado_update(request, pk):
    empregado = Empregado.objects.get(pk=pk)
    setor_id = empregado.setor_id
    funcao_id = empregado.funcao_id
    grupo_id = empregado.grupo_id
    setores = Setor.objects.all().order_by('nome')
    funcoes = Funcao.objects.all().filter(id=funcao_id)
    grupos = Grupo.objects.all().filter(id=grupo_id)
    # form = EmpregadoForm(request.POST or None, instance=empregado)
    data = {
        'empregado': empregado,
        'setores': setores,
        'funcoes': funcoes,
        'grupos': grupos,
        # 'form': form,
    }
    if request.method == 'POST':
        empregado.nome = request.POST.get('nome')
        empregado.cpf = request.POST.get('cpf')
        empregado.serie = request.POST.get('serie')
        empregado.ctps = request.POST.get('ctps')
        data_nascimento = request.POST.get('data_nascimento')
        dia = data_nascimento[0:2]
        mes = data_nascimento[3:5]
        ano = data_nascimento[6:10]
        empregado.data_nascimento = str(ano) + '-' + str(mes) + '-' + str(dia)
        data_inicio = request.POST.get('data_admissao')
        dia = data_inicio[0:2]
        mes = data_inicio[3:5]
        ano = data_inicio[6:10]
        empregado.data_inicio = str(ano) + '-' + str(mes) + '-' + str(dia)
        data_fim = request.POST.get('data_demissao')
        empregado.grupo_id = request.POST.get('grupo_id')
        empregado.setor_id = request.POST.get('setor_id')
        empregado.funcao_id = request.POST.get('funcao_id')
        if data_fim == '':
            empregado.data_fim = None
            empregado.save()
        else:
            dia = data_fim[0:2]
            mes = data_fim[3:5]
            ano = data_fim[6:10]
            empregado.data_fim = str(ano) + '-' + str(mes) + '-' + str(dia)
            empregado.save()
        messages.success(request, 'Registro alterado com sucesso')
        return redirect("lista_empregados")
    else:
        return render(request, 'empregado_update.html', data)


@login_required
def empregado_delete(request, pk):
    empregado = Empregado.objects.get(pk=pk)
    empregado.delete()
    messages.success(request, 'Registro Excluido com sucesso')
    return redirect('lista_empregados')


@login_required
def lista_coords(request):
    coords = Coordenador.objects.all().order_by('-data_inicio')
    data = {
        'coords': coords,
    }
    return render(request, 'lista_coords.html', data)


@login_required
def coord_novo(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        crm = request.POST.get('crm')
        data_admissao = request.POST.get('data_admissao')
        dia = data_admissao[0:2]
        mes = data_admissao[3:5]
        ano = data_admissao[6:10]
        data_admissao = str(ano) + '-' + str(mes) + '-' + str(dia)
        data_demissao = request.POST.get('data_demissao')
        count = Coordenador.objects.filter(nome=nome, crm=crm).count()
        if count > 0:
            messages.error(request, 'Coordenador ja cadastrado com este Nome e CRM')
            return redirect('coord_novo')
        else:
            if data_demissao == '':
                c = Coordenador.objects.create(
                    nome=nome,
                    crm=crm,
                    data_inicio=data_admissao,
                    data_fim=None
                )
            else:
                dia = data_demissao[0:2]
                mes = data_demissao[3:5]
                ano = data_demissao[6:10]
                data_demissao = str(ano) + '-' + str(mes) + '-' + str(dia)
                c = Coordenador.objects.create(
                    nome=nome,
                    crm=crm,
                    data_inicio=data_admissao,
                    data_fim=data_demissao
                )
            messages.success(request, 'Registro Cadastrado com sucesso')
            return redirect("lista_coords")
    else:
        form = CoordenadorForm
        data = {
            'form': form,
        }
        return render(request, 'coord_novo.html', data)


@login_required
def coord_update(request, pk):
    coord = Coordenador.objects.get(pk=pk)
    data = {
        'coord': coord,
    }
    if request.method == 'POST':
        coord.nome = request.POST.get('nome')
        coord.cpf = request.POST.get('cpf')
        data_inicio = request.POST.get('data_admissao')
        dia = data_inicio[0:2]
        mes = data_inicio[3:5]
        ano = data_inicio[6:10]
        coord.data_inicio = str(ano) + '-' + str(mes) + '-' + str(dia)
        data_fim = request.POST.get('data_demissao')
        if data_fim == '':
            coord.data_fim = None
            coord.save()
        else:
            dia = data_fim[0:2]
            mes = data_fim[3:5]
            ano = data_fim[6:10]
            coord.data_fim = str(ano) + '-' + str(mes) + '-' + str(dia)
            coord.save()
        messages.success(request, 'Registro alterado com sucesso')
        return redirect("lista_coords")
    else:
        return render(request, 'coord_update.html', data)


@login_required
def coord_delete(request, pk):
    coord = Coordenador.objects.get(pk=pk)
    coord.delete()
    messages.success(request, 'Registro Excluido com sucesso')
    return redirect('lista_coords')


# Comeco riscos keywords atendimentos atendimento Atendimento
@login_required
def lista_atendimentos(request):
    form = AtendimentoForm
    atendimentos_list = Atendimento.objects.all().order_by('-data_atendimento')
    paginator = Paginator(atendimentos_list, 10)
    page = request.GET.get('page')
    atendimentos = paginator.get_page(page)
    data = {
        'atendimentos': atendimentos,
        'form': form
    }
    return render(request, 'lista_atendimentos.html', data)


@login_required
def atendimento_novo(request):
    empregados = Empregado.objects.all().order_by('nome')
    tipoexames = TipoExame.objects.all().order_by('nome')
    if request.method == 'POST':
        empregado_id = request.POST.get('empregado_id')
        tipoexame_id = request.POST.get('tipoexame_id')
        data_atendimento = request.POST.get('data_atendimento')
        dia = data_atendimento[0:2]
        mes = data_atendimento[3:5]
        ano = data_atendimento[6:10]
        data_atendimento = str(ano) + '-' + str(mes) + '-' + str(dia)
        trabalhoaltura = request.POST.get('altura')
        if trabalhoaltura == "on":
            trabalhoaltura = 1
        else:
            trabalhoaltura = 0
        espacoconfinado = request.POST.get('espaco')
        if espacoconfinado == "on":
            espacoconfinado = 1
        else:
            espacoconfinado = 0
        apto = request.POST.get('apto')
        if apto == "on":
            apto = 1
        else:
            apto = 0
        empregado = Empregado.objects.get(id=empregado_id)
        grupo_id = empregado.grupo_id
        setor_id = empregado.setor_id
        funcao_id = empregado.funcao_id
        coordenador = Coordenador.objects.get(data_fim=None)
        coordenador_id = coordenador.id
        e = Atendimento.objects.create(
            empregado_id=empregado_id,
            coordenador_id=coordenador_id,
            tipoexame_id=tipoexame_id,
            data_atendimento=data_atendimento,
            trabalhoaltura=trabalhoaltura,
            espacoconfinado=espacoconfinado,
            apto=apto,
            grupo_id=grupo_id,
            setor_id=setor_id,
            funcao_id=funcao_id,
        )
        atendimento_id = Atendimento.objects.latest('pk').pk
        gruporiscos = GrupoRisco.objects.all().filter(grupo_id=grupo_id)
        for gruporisco in gruporiscos:
            a = AtendimentoRisco.objects.create(
                atendimento_id=atendimento_id,
                risco_id=gruporisco.risco.id,
            )
        grupoexames = GrupoExame.objects.all().filter(grupo_id=grupo_id)
        for grupoexame in grupoexames:
            a = AtendimentoExame.objects.create(
                atendimento_id=atendimento_id,
                exame_id=grupoexame.exame.id,
            )
        messages.success(request, "Registro cadastrado com sucesso !")
        return redirect('lista_atendimentos')
    else:
        form = AtendimentoForm
        data = {
            'form': form,
            'empregados': empregados,
            'tipoexames': tipoexames,
        }
        return render(request, 'atendimento_novo.html', data)
    # return render(request,'home')


@login_required
def atendimento_update(request, pk):
    atendimento = Atendimento.objects.get(pk=pk)
    empregado_id = atendimento.empregado_id
    grupo_id = atendimento.grupo_id
    setor_id = atendimento.setor_id
    funcao_id = atendimento.empregado_id
    empregados = Empregado.objects.all().filter(id=empregado_id)
    tipoexames = TipoExame.objects.all().order_by('nome')
    form = AtendimentoForm(request.POST or None, instance=atendimento)
    data = {
        'empregados': empregados,
        'tipoexames': tipoexames,
        'atendimento': atendimento,
        'form': form,
    }
    if request.method == 'POST':
        tipoexame_id = str(request.POST.get('tipoexame_id'))
        tipoexame_anterior_id = str(atendimento.tipoexame_id)
        trabalhoaltura = request.POST.get('altura')
        if trabalhoaltura == "on":
            atendimento.trabalhoaltura = 1
        else:
            atendimento.trabalhoaltura = 0
        espacoconfinado = request.POST.get('espaco')
        if espacoconfinado == "on":
            atendimento.espacoconfinado = 1
        else:
            atendimento.espacoconfinado = 0
        apto = request.POST.get('apto')
        if apto == "on":
            atendimento.apto = 1
        else:
            atendimento.apto = 0
        data_atendimento = request.POST.get('data_atendimento')
        dia = data_atendimento[0:2]
        mes = data_atendimento[3:5]
        ano = data_atendimento[6:10]
        atendimento.data_atendimento = str(ano) + '-' + str(mes) + '-' + str(dia)
        atendimento.grupo_id = grupo_id
        atendimento.setor_id = setor_id
        atendimento.funcao_id = funcao_id
        if tipoexame_anterior_id == tipoexame_id:
            deletou = False
        else:
            AtendimentoRisco.objects.all().filter(atendimento_id=pk).delete()
            AtendimentoExame.objects.all().filter(atendimento_id=pk).delete()
            deletou = True
        atendimento.tipoexame_id = tipoexame_id
        atendimento.save()

        if deletou:
            riscos = GrupoRisco.objects.all().filter(grupo_id=grupo_id)
            exames = GrupoExame.objects.all().filter(grupo_id=grupo_id, tipoexame_id=tipoexame_id)
            for risco in riscos:
                a = AtendimentoRisco.objects.create(
                    atendimento_id=pk,
                    risco_id=risco.risco.id,
                )
            for exame in exames:
                a = AtendimentoExame.objects.create(
                    atendimento_id=pk,
                    exame_id=exame.exame.id,
                )
        messages.success(request, 'Registro alterado com sucesso')
        return redirect('lista_atendimentos')
    else:
        return render(request, 'atendimento_update.html', data)


@login_required
def atendimento_search(request):
    nome = request.GET.get('nome')
    data1 = request.GET.get('data1')
    data2 = request.GET.get('data2')
    if data2 == '':
        data2 = data1
    if nome == '':
        if data1 == '':
            messages.error(request, 'Informe pelo menos uma condicao de pesquisa!')
            return redirect('lista_atendimentos')
        else:
            atendimentos = Atendimento.objects.filter(data_atendimento__range=[data1, data2])
    else:
        if data1 == '':
            atendimentos = Atendimento.objects.filter(empregado__nome__icontains=nome)
        else:
            a = Atendimento.objects.filter(empregado__nome__icontains=nome)
            atendimentos = a.filter(data_atendimento__range=[data1, data2])
    form = AtendimentoForm()
    return render(request, 'lista_atendimentos.html', {'form': form, 'atendimentos': atendimentos})


@login_required
def atendimento_delete(request, pk):
    atendimento = Atendimento.objects.get(pk=pk)
    AtendimentoRisco.objects.all().filter(atendimento_id=pk).delete()
    AtendimentoExame.objects.all().filter(atendimento_id=pk).delete()
    atendimento.delete()
    messages.success(request, 'Registro Excluido com sucesso')
    return redirect('lista_atendimentos')


@login_required
def atendimentorisco_novo(request, pk):
    atendimento = Atendimento.objects.get(pk=pk)
    riscos = Risco.objects.all().order_by('nome')
    atendimentoriscos = AtendimentoRisco.objects.filter(atendimento_id=pk)
    data = {
        'atendimento': atendimento,
        'riscos': riscos,
        'atendimentoriscos': atendimentoriscos,
    }
    if request.method == 'POST':
        risco_id = request.POST.get('risco_id')
        count = AtendimentoRisco.objects.filter(atendimento_id=pk, risco_id=risco_id).count()
        if count > 0:
            messages.error(request, 'Registro ja cadastrado')
            return redirect('/atendimentorisco_novo/' + str(pk))
        else:
            a = AtendimentoRisco.objects.create(
                atendimento_id=pk,
                risco_id=risco_id
            )
            return redirect('/atendimentorisco_novo/' + str(pk))

    else:
        return render(request, 'atendimentorisco_novo.html', data)


@login_required
def atendimentorisco_delete(request, pk):
    atendimentorisco = AtendimentoRisco.objects.all().filter(id=pk)
    atendimento_id = atendimentorisco.atendimento_id
    atendimentorisco.delete()
    return redirect('/atendimentorisco_novo/' + str(atendimento_id))


@login_required
def atendimentoexame_novo(request, pk):
    atendimento = Atendimento.objects.get(pk=pk)
    exames = Exame.objects.all().order_by('nome')
    atendimentoexames = AtendimentoExame.objects.filter(atendimento_id=pk)
    data = {
        'atendimento': atendimento,
        'exames': exames,
        'atendimentoexames': atendimentoexames,
    }
    if request.method == 'POST':
        exame_id = request.POST.get('exame_id')
        count = AtendimentoExame.objects.filter(atendimento_id=pk, exame_id=exame_id).count()
        if count > 0:
            messages.error(request, 'Registro ja cadastrado')
            return redirect('/atendimentoexame_novo/' + str(pk))
        else:
            a = AtendimentoExame.objects.create(
                atendimento_id=pk,
                exame_id=exame_id
            )
            return redirect('/atendimentoexame_novo/' + str(pk))

    else:
        return render(request, 'atendimentoexame_novo.html', data)


@login_required
def atendimentoexame_delete(request, pk):
    atendimentoexame = AtendimentoExame.objects.all().filter(id=pk)
    atendimento_id = atendimentoexame.atendimento_id
    atendimentoexame.delete()
    return redirect('/atendimentoexame_novo/' + str(atendimento_id))


# @login_required
# def rel_aso(request, pk):
#     atendimento = Atendimento.objects.get(id=pk)
#     exames = Exame.objects.filter(atendimento_id=pk)
#     riscos = Risco.objects.filter(atendimento_id=pk)
#     data = {
#         'atendimento': atendimento,
#         'exames': exames,
#         'riscos': riscos,
#         'request': request,
#     }
#     return Render.render('rel_aso.html', data, 'rel_aso')

# class Render:
#     @staticmethod
#     def render(path: str, data: dict, filename: str):
#         template = get_template(path)
#         html = template.render(data)
#         response = io.BytesIO()
#         pdf = pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), response)
#         if pdf.err:
#             return HttpResponse('We had some errors')
#         return response


@login_required
def atendimento_pdf(request, pk):
    data = []
    lista_riscos = []
    lista_exames = []
    dicionario = {}
    atendimento = Atendimento.objects.get(id=pk)
    atendimento_exame = AtendimentoExame.objects.all().filter(atendimento_id=atendimento.pk)
    atendimento_risco = AtendimentoRisco.objects.all().filter(atendimento_id=atendimento.pk)
    nome = atendimento.empregado.nome
    tipo_exame = atendimento.tipoexame
    data_atendimento = atendimento.data_atendimento
    setor = atendimento.empregado.setor
    funcao = atendimento.empregado.funcao
    altura = atendimento.trabalhoaltura
    espaco = atendimento.espacoconfinado
    apto = atendimento.apto
    dicionario['atendimento'] = atendimento.pk
    dicionario['nome'] = nome
    dicionario['tipo_exame'] = tipo_exame.nome
    dicionario['data_atendimento'] = data_atendimento
    dicionario['setor'] = setor.nome
    dicionario['funcao'] = funcao.nome
    dicionario['altura'] = altura
    dicionario['espaco'] = espaco
    dicionario['apto'] = apto
    for risco in atendimento_risco:
        lista_riscos.append({'risco': risco.risco.nome})
    for exame in atendimento_exame:
        lista_exames.append({'exame': exame.exame.nome})
    dicionario['riscos'] = lista_riscos
    dicionario['exames'] = lista_exames
    # data.append(dicionario)
    # print(data)
    # for risco, ind in enumerate(atendimento_risco):
    #     if ind == 0:
    #         dicionario['risco'] = risco
    #     else:
    #         data.append({'risco': risco})
    # for exame, ind in enumerate(atendimento_exame):
    #     if ind == 0:
    #         dicionario['exame'] = exame
    # else:
    #     if data[ind] != '':
    #         data[ind]['exame'] = exame
    # else:
    #     data.append({'exame': exame})
    # data.insert(0, dicionario)
    return report(request, 'atendimento', dicionario)
