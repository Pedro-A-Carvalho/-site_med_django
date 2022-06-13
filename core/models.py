from django.db import models

# Create your models here.


class Funcao(models.Model):
    nome = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'funcao'


class Setor(models.Model):
    nome = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'setor'


class TipoRisco(models.Model):
    nome = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'tiporisco'


class Risco(models.Model):
    nome = models.CharField(max_length=50, blank=False, null=False)
    tiporisco = models.ForeignKey(TipoRisco, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'risco'


class Grupo(models.Model):
    nome = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'grupo'


class Exame(models.Model):
    nome = models.CharField(max_length=50, blank=False, null=False)
    validade = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'exame'


class TipoExame(models.Model):
    nome = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'tipoexame'


class GrupoExame(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT)
    exame = models.ForeignKey(Exame, on_delete=models.PROTECT)
    tipoexame = models.ForeignKey(TipoExame, on_delete=models.PROTECT)

    class Meta:
        db_table = 'grupoexame'


class GrupoFuncao(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT)
    funcao = models.ForeignKey(Funcao, on_delete=models.PROTECT)
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT)

    class Meta:
        db_table = 'grupofuncao'


class GrupoRisco(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT)
    risco = models.ForeignKey(Risco, on_delete=models.PROTECT)

    class Meta:
        db_table = 'gruporisco'


class Coordenador(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False)
    crm = models.CharField(max_length=50, null=False, blank=False)
    data_inicio = models.DateField(null=False, blank=False)
    data_fim = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'coordenador'


class Empregado(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False)
    cpf = models.CharField(max_length=15, null=False, blank=False)
    ctps = models.CharField(max_length=20, null=False, blank=False)
    serie = models.CharField(max_length=10, null=False, blank=False)
    data_nascimento = models.DateField(null=False, blank=False)
    data_inicio = models.DateField(null=False, blank=False)
    data_fim = models.DateField(null=True, blank=True)
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT)
    funcao = models.ForeignKey(Funcao, on_delete=models.PROTECT)
    grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT)

    class Meta:
        db_table = 'empregado'


class Atendimento(models.Model):
    data_atendimento = models.DateField(null=False, blank=False)
    empregado = models.ForeignKey(Empregado, on_delete=models.PROTECT)
    coordenador = models.ForeignKey(Coordenador, on_delete=models.PROTECT)
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT)
    funcao = models.ForeignKey(Funcao, on_delete=models.PROTECT)
    grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT)
    tipoexame = models.ForeignKey(TipoExame, on_delete=models.PROTECT)
    trabalhoaltura = models.BooleanField()
    espacoconfinado = models.BooleanField()
    apto = models.BooleanField()

    class Meta:
        db_table = 'atendimento'


class AtendimentoRisco(models.Model):
    atendimento = models.ForeignKey(Atendimento, on_delete=models.PROTECT)
    risco = models.ForeignKey(Risco, on_delete=models.PROTECT)

    class Meta:
        db_table = 'atendimentorisco'


class AtendimentoExame(models.Model):
    atendimento = models.ForeignKey(Atendimento, on_delete=models.PROTECT)
    exame = models.ForeignKey(Exame, on_delete=models.PROTECT)

    class Meta:
        db_table = 'atendimentoexame'



