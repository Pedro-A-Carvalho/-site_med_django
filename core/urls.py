from django.contrib import admin
from django.urls import path
from .views import home, lista_funcoes, funcao_novo, funcao_update, funcao_search, funcao_delete, lista_setores, setor_novo, setor_update, setor_search, setor_delete
from .views import lista_tipo_riscos, tipo_risco_novo, tipo_risco_update, tipo_risco_delete
from .views import lista_riscos, risco_novo, risco_update, risco_search, risco_delete
from .views import lista_exames, exame_novo, exame_update, exame_search, exame_delete
from .views import lista_grupos, grupo_novo, grupo_update, grupo_delete, grupofuncao_novo, grupofuncao_delete
from .views import gruporisco_novo, gruporisco_delete, grupoexame_novo, grupoexame_delete
from .views import lista_empregados, empregado_novo, empregado_update, empregado_delete, load_funcoes, load_grupos
from .views import lista_coords, coord_novo, coord_update, coord_delete
from .views import lista_atendimentos, atendimento_novo, atendimento_update, atendimento_delete, atendimento_search
from .views import atendimentorisco_novo, atendimentorisco_delete
from .views import atendimentoexame_novo, atendimentoexame_delete
# from .views import rel_aso
from django.contrib.auth import views as auth_view
from .views import alterar_senha, atendimento_pdf
from .views import ListaFuncoes, FuncaoNovo, FuncaoUpdate, ListaEmpregados, EmpregadoNovo


urlpatterns = [
    path('alterar_senha', alterar_senha, name='alterar_senha'),

    path('atendimento_pdf/<int:pk>', atendimento_pdf, name='atendimento_pdf'),

    path('', home, name='home'),
    # path('lista_funcoes', lista_funcoes, name='lista_funcoes'),
    path('lista_funcoes', ListaFuncoes.as_view(), name='lista_funcoes'),
    # path('funcao_novo', funcao_novo, name='funcao_novo'),
    path('funcao_novo', FuncaoNovo.as_view(), name='funcao_novo'),
    # path('funcao_update/<int:pk>', funcao_update, name='funcao_update'),
    path('funcao_update/<int:pk>', FuncaoUpdate.as_view(), name='funcao_update'),
    path('funcao_search', funcao_search, name='funcao_search'),
    path('funcao_delete/<int:pk>', funcao_delete, name='funcao_delete'),

    path('lista_setores', lista_setores, name='lista_setores'),
    path('setor_novo', setor_novo, name='setor_novo'),
    path('setor_update/<int:pk>', setor_update, name='setor_update'),
    path('setor_search', setor_search, name='setor_search'),
    path('setor_delete/<int:pk>', setor_delete, name='setor_delete'),

    path('lista_tipo_riscos', lista_tipo_riscos, name='lista_tipo_riscos'),
    path('tipo_risco_novo', tipo_risco_novo, name='tipo_risco_novo'),
    path('tipo_risco_update/<int:pk>', tipo_risco_update, name='tipo_risco_update'),
    path('tipo_risco_delete/<int:pk>', tipo_risco_delete, name='tipo_risco_delete'),

    path('lista_riscos', lista_riscos, name='lista_riscos'),
    path('risco_novo', risco_novo, name='risco_novo'),
    path('risco_update/<int:pk>', risco_update, name='risco_update'),
    path('risco_search', risco_search, name='risco_search'),
    path('risco_delete/<int:pk>', risco_delete, name='risco_delete'),

    path('lista_exames', lista_exames, name='lista_exames'),
    path('exame_novo', exame_novo, name='exame_novo'),
    path('exame_update/<int:pk>', exame_update, name='exame_update'),
    path('exame_search', exame_search, name='exame_search'),
    path('exame_delete/<int:pk>', exame_delete, name='exame_delete'),

    path('lista_grupos', lista_grupos, name='lista_grupos'),
    path('grupo_novo', grupo_novo, name='grupo_novo'),
    path('grupo_update/<int:pk>', grupo_update, name='grupo_update'),
    path('grupo_delete/<int:pk>', grupo_delete, name='grupo_delete'),
    path('grupofuncao_novo/<int:pk>', grupofuncao_novo, name='grupofuncao_novo'),
    path('grupofuncao_delete/<int:pk>', grupofuncao_delete, name='grupofuncao_delete'),
    path('gruporisco_novo/<int:pk>', gruporisco_novo, name='gruporisco_novo'),
    path('gruporisco_delete/<int:pk>', gruporisco_delete, name='gruporisco_delete'),
    path('grupoexame_novo/<int:pk>', grupoexame_novo, name='grupoexame_novo'),
    path('grupoexame_delete/<int:pk>', grupoexame_delete, name='grupoexame_delete'),

    # path('lista_empregados', lista_empregados, name='lista_empregados'),
    path('lista_empregados', ListaEmpregados.as_view(), name='lista_empregados'),
    # path('empregado_novo', empregado_novo, name='empregado_novo'),
    path('empregado_novo', EmpregadoNovo.as_view(), name='empregado_novo'),
    path('empregado_update/<int:pk>', empregado_update, name='empregado_update'),
    path('ajax/load-funcoes', load_funcoes, name='ajax_load_funcoes'),
    path('ajax/load-grupos', load_grupos, name='ajax_load_grupos'),
    path('empregado_delete/<int:pk>', empregado_delete, name='empregado_delete'),

    path('lista_coords', lista_coords, name='lista_coords'),
    path('coord_novo', coord_novo, name='coord_novo'),
    path('coord_update/<int:pk>', coord_update, name='coord_update'),
    path('coord_delete/<int:pk>', coord_delete, name='coord_delete'),

    path('lista_atendimentos', lista_atendimentos, name='lista_atendimentos'),
    path('atendimento_novo', atendimento_novo, name='atendimento_novo'),
    path('atendimento_update/<int:pk>', atendimento_update, name='atendimento_update'),
    path('atendimento_delete/<int:pk>', atendimento_delete, name='atendimento_delete'),
    path('atendimento_search', atendimento_search, name='atendimento_search'),
    path('atendimentorisco_novo/<int:pk>', atendimentorisco_novo, name='atendimentorisco_novo'),
    path('atendimentorisco_delete/<int:pk>', atendimentorisco_delete, name='atendimentorisco_delete'),
    path('atendimentoexame_novo/<int:pk>', atendimentoexame_novo, name='atendimentoexame_novo'),
    path('atendimentoexame_delete/<int:pk>', atendimentoexame_delete, name='atendimentoexame_delete'),
    # path('rel_aso/<int:pk>', rel_aso, name='rel_aso'),

]