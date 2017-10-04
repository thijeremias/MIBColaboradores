#-*-coding: utf8 -*-
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import Colaborador, Franquia
from .forms import ColaboradorForm
from .forms import userLogin
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

#View de login de usuários no sistema, segue modelo da documentação do django
def do_login(request):
	if request.method == 'POST':
		user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
		if user is not None:
			login(request, user)
			return redirect('home')
	#user = userLogin()
	return render(request, 'mibcolaboradores/login.html',{'user': user})	

#View para cadastrar novos colaboradores
@login_required 
def cadastrar(request):
	context = {}
	if request.method == 'POST':
		form = ColaboradorForm(request.POST)
		if form.is_valid():
			colaborador = form.save(commit = False)#colaborador não é salvo agora
			context['is_valid'] = True #Controle para o template saber se está adicionando ou não um formulário ao banco de dados
			grupos = request.user.groups.all()
			for grupo in grupos:
				a = str(grupo)
			colaborador.colaborador_franquia = Franquia.objects.get(franquia_descricao = a) #Franquia adicionada automaticamente de acordo com o grupo do usuário
			colaborador.save()#Agora sim o colaborador é salvo
			form = ColaboradorForm()
			context['form'] = form
			return render(request, 'mibcolaboradores/cadastrar.html', context)
		else:
			context['form'] = form
			return render(request, 'mibcolaboradores/cadastrar.html', context)
	else:
		form = ColaboradorForm()
		context['form'] = form
		return render(request, 'mibcolaboradores/cadastrar.html', context)

#Página inicial do sistema, apresenta dashboard com os limites da franquia em logada
@login_required
def home(request):
	context = {}
	a = ''
	grupos = request.user.groups.all() #Captura os grupos do usuário. Nesse sistema o usuário terá apenas um grupo
	for grupo in grupos:
		a = str(grupo)#Armazena em a o nome do grupo do usuário
	context['grupo'] = a#Passa o nome do grupo como contexto para o template
	franquia = get_object_or_404(Franquia, franquia_descricao = a)#Captura a franquia logada
	context['franquia'] = franquia#Passo para o template a franquia logada
	context['caixa_limite'] = 0#Variáveis com os valores de limite da franquia são zeradas 
	context['vendedor_limite'] = 0
	context['estoquista_limite'] = 0
	context['crediarista_limite'] = 0
	context['servicos_limite'] = 0
	context['administrativo_limite'] = 0
	for colaborador in Colaborador.objects.all(): #Pego todos os colaboradores
		if str(colaborador.colaborador_franquia) == a and colaborador.colaborador_demissao is None: #Verifico se o colaborador pertence a franquia logada e se o funcionário é ativo
			if str(colaborador.colaborador_funcao) == 'Caixa':#utilizo um aninhamento de if para decidir a função do coloaborador
				context['caixa_limite'] += 1
			elif str(colaborador.colaborador_funcao) == 'Vendedor':
				   context['vendedor_limite'] += 1
			elif str(colaborador.colaborador_funcao) == 'Crediarista':
				   context['crediarista_limite'] += 1
			elif str(colaborador.colaborador_funcao) == 'Estoquista':
				   context['estoquista_limite'] += 1
			elif str(colaborador.colaborador_funcao) == 'Servicos Gerais':
				   context['servicos_limite'] += 1
			elif str(colaborador.colaborador_funcao) == 'Administrativo':
				   context['administrativo_limite'] += 1
#as funções são incrementadas e passadas ao template	 
	return render(request, 'mibcolaboradores/home.html', context)

#View para fazer logout dos usuários, segue modelo da documentação do django
def do_logout(request):
	logout(request)
	return redirect('login')

#View para consultar colaboradores
@login_required
def consultar(request):
	context = {}
	if request.method == 'POST':
		grupos = request.user.groups.all()
		for grupo in grupos:
			  a = grupo.id
	    #Pego os colaboradores que fazem parte da franquia logada por nome ou cpf
		var = Colaborador.objects.search(request.POST.get('colaborador_nome')).filter(colaborador_franquia = a).order_by('colaborador_nome')
		context['controle'] = 1 #Controle para template 
		context['form'] = var #contexto com os colaboradores encontrados
		return render(request,'mibcolaboradores/consultar.html', context)
	else:
		var = ColaboradorForm()
		context['form'] = var
		return render(request, 'mibcolaboradores/consultar.html',context)

@login_required
def editar(request, pk):#Recebe a pk na solicitação da url
	context = {}
	var = get_object_or_404(Colaborador, pk=pk)#Pego no BD o colaborador específico
	if request.method == "POST":#Se verdadeiro significa que o colaborador já foi editado e então precisa ser salvo
		form = ColaboradorForm(request.POST, instance = var)#form recebe o formulário com as edições
		if form.is_valid():#Verifica se o formulário é válido
			colaborador = form.save(commit = False)#Não salva ainda
			grupos = request.user.groups.all()
			for grupo in grupos:
				a = str(grupo)
			colaborador.colaborador_franquia = Franquia.objects.get(franquia_descricao = a)#Adiciono a franquia ao colaborador
			colaborador.save()#Salvo o colaborador
			context['controle'] = 2 #Controle para o template saber se vai consultar ou exibir uma mensagem de êxito da última alteração
			return render(request, 'mibcolaboradores/consultar.html', context)
		else:
			context['form'] = form
			return render(request, 'mibcolaboradores/editar.html', context)
	else:
		form = ColaboradorForm(instance = var)#Se falso a página é aberta com os dados do colaborador	
		return render(request, 'mibcolaboradores/editar.html', {'form': form})