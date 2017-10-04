#-*-coding: utf8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from datetime import date

class ColaboradorManager(models.Manager):#Manager para fazer consultas em colaboradores
	
	def search(self, query):
		return self.get_queryset().filter(
			models.Q(colaborador_nome__icontains = query) | 
			models.Q(colaborador_cpf__icontains = query) 
			)

class Funcao (models.Model):#Classe que armazena somente as funções dos colaboradores
	funcao_descricao = models.CharField('Função', max_length = 25)
	
	class Meta:
		verbose_name = 'Função'
		verbose_name_plural = 'Funções'
	
	def __str__ (self):#Função que retorna a descrição da função
		return self.funcao_descricao

class Franquia (models.Model):#Classe para armazenar franquias e seus limites de colaboradores
	franquia_descricao = models.CharField('Franquia', max_length = 11)
	#franquia_limite_caixa = models.IntegerField('Limite Caixa', default = 4)
	
	franquia_limite_vendedor = models.IntegerField('Limite Vendedor', default = 8)
	franquia_limite_administrativo = models.IntegerField('Limite Administrativo', default = 1)
	franquia_limite_estoquista = models.IntegerField('Limite Estoquista', default = 1)
	franquia_limite_crediarista = models.IntegerField('Limite Crediarista', default = 2)
	franquia_limite_servicos = models.IntegerField('Limite Serviços Gerais', default = 1)
	
	def __str__ (self):#Função que retorna a descrição da franquia
		return self.franquia_descricao
	
	
class Colaborador (models.Model):#Classe que armazenará os colaboradores
	
	SEXO_CHOICES = ( #Choices para sexo, apresenta uma lista para escolha

		('masculino', 'Masculino'),#Opções, primeiro campo BD, segundo campo como o usuário verá
		('feminino', 'Feminino'),

	)
	
	
	
	colaborador_nome = models.CharField('Nome', max_length = 50)
	colaborador_cpf = models.CharField('CPF', max_length = 11, unique = True)#Atributo cpf como único no BD
	colaborador_sexo = models.CharField('Sexo', max_length = 11, choices = SEXO_CHOICES, default = 'masculino')#No atributo sexo incluimos o choices para escolha
	colaborador_nascimento = models.DateField('Data de Nascimento')
	colaborador_admissao = models.DateField('Data de Admissão', default = date.today())#Atributo data admissão tem como default a data do dia
	colaborador_demissao = models.DateField('Data de Demissão', blank = True, null = True)#Atributo demissão pode ser nulo, blank para forms e null para BD	
	colaborador_ativo = models.BooleanField('Ativo', default = True)
	colaborador_funcao = models.ForeignKey(Funcao, on_delete = models.CASCADE)#Chave estrangeira para a classe Funcao
	colaborador_franquia = models.ForeignKey(Franquia, on_delete = models.CASCADE, blank = True)#Chave estrangeira para a classe Franquia	objects = ColaboradorManager()
	objects = ColaboradorManager()
	
	class Meta:
		verbose_name = 'Colaborador'
		verbose_name_plural = 'Colaboradores'
		
	def __str__ (self):#Função que retorna o nome do colaborador
		return self.colaborador_nome
		

	
	
	

