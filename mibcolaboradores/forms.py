#-*-coding: utf8 -*-
from django import forms
from .models import Colaborador
from django.contrib.auth.models import User
from datetime import date
from localflavor.br.forms import BRCPFField #Pacote para fazer validação do cpf. Deve ser instalado a parte
from django.core.mail import send_mail
from django.conf import settings


#Formulário do colaborador
class ColaboradorForm(forms.ModelForm):
	colaborador_cpf = BRCPFField(max_length = 11, min_length = 11) #Validação do CPF
	class Meta:
		model = Colaborador #formulário recebe a classe Colaborador como modelo
		fields = ('colaborador_nome', 'colaborador_cpf', 'colaborador_funcao', 'colaborador_nascimento', 'colaborador_sexo', 
			'colaborador_admissao', 'colaborador_demissao', 'colaborador_franquia', 'colaborador_ativo',
			)#Campos que serão usados no formulário
		widgets = {
			'colaborador_franquia': forms.TextInput(attrs = {'readonly': True}),#Torna essa campo não editável, não está em uso no momento
            'colaborador_sexo': forms.RadioSelect,#Transforma a lista de escolha do choices em Radio Button
		}
		#função para enviar e-mails, quando um colaborador é adicionado ou demitido
	def send_mail(self, colaborador):
		subject = 'Colaborador Adicionado na %s' %colaborador.colaborador_franquia 
		mensagem = "Colaborador: '{0}';\nFunção: '{1}';\nCPF: '{2}'.".format(colaborador.colaborador_nome, colaborador.colaborador_funcao, colaborador.colaborador_cpf)
		if colaborador.colaborador_demissao:
			subject = 'Colaborador Demitido na %s' %colaborador.colaborador_franquia
			mensagem += '\nData de demissão: %s' %colaborador.colaborador_demissao
		else:
			mensagem += '\nData de admissão: %s' %colaborador.colaborador_admissao
		send_mail(subject,mensagem,settings.SERVER_EMAIL,settings.DEFAULT_TO_EMAIL,fail_silently=False,)
	


#Formulário de login do django
class userLogin(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password']
		widgets = {
			'username': forms.TextInput(attrs = {'class': 'form-control', 'maxlength': 255}),
			'password': forms.PasswordInput(attrs = {'class': 'form-control', 'maxlength': 255}),		
		}