#-*-coding: utf8 -*-
import json
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import Colaborador, Franquia, Funcao
from .forms import ColaboradorForm, send_mail, userLogin
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

#View de login de usuários no sistema, segue modelo da documentação do django
def do_login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('administrativo')
            else:
                return redirect('home')
    user = userLogin()
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
            
            #Uso o grupo para saber a franquia do usuário
            grupos = request.user.groups.all()
            for grupo in grupos:
                a = str(grupo)
            
            """Busco todas as franquias de acordo com o grupo, os colaboradores terão sempre a primeira franquia
               encontrada """        
            for franquia in Franquia.objects.all():
                if franquia.franquia_descricao == a:
                    colaborador.colaborador_franquia = franquia
                    break
            
            #envio e-mail com o colaborador cadastrado
            form.send_mail(colaborador)
            
            colaborador.save()#Agora sim o colaborador é salvo
            form = ColaboradorForm()#Um novo formulário em branco é enviado ao template
            context['form'] = form
            return render(request, 'mibcolaboradores/cadastrar.html', context)
        else:
            #caso formulário não seja válido é apresentado novamente com os erros
            context['form'] = form
            return render(request, 'mibcolaboradores/cadastrar.html', context)
    else:
        #se o metodo não for post é apresentado formulário em branco para cadastro
        form = ColaboradorForm()
        context['form'] = form
        return render(request, 'mibcolaboradores/cadastrar.html', context)

"""Página inicial do sistema, apresenta dashboard com função, limites e quantidade de colaboradores
   para a franquia logada """
@login_required
def home(request):
    context = {}
    a = '' #variável utilizada para armazenar a franquia obtida pelo grupo do usuário
    b = 0 #variável utilizada para armazenar o id da franquia logada, sempre será a primeira franquia encontrada
    
    #Uso o grupo para saber a franquia do usuário
    grupos = request.user.groups.all() 
    for grupo in grupos:
        a = str(grupo)
    context['grupo'] = a#Passa o nome do grupo como contexto para o template
    
    """Busco todas as franquias de acordo com o grupo, os colaboradores terão sempre a primeira franquia
               encontrada """        
    for franquia in Franquia.objects.all():
        if franquia.franquia_descricao == a:
            b = franquia.id
            break
            
    #Passo todos os colaboradores da franquia logada para o template            
    context['colaboradores'] = Colaborador.objects.filter(colaborador_franquia = b)
    #Passo todas as franquias com funções de acordo com a franquia logada
    context['franquias'] = Franquia.objects.all().filter(franquia_descricao = a)
    return render(request, 'mibcolaboradores/home.html', context)

#View para fazer logout dos usuários, segue modelo da documentação do django
def do_logout(request):
    logout(request)
    return redirect('login')

#View para consultar colaboradores
@login_required
def consultar(request):
    context = {}
    
    #Declaro uma lista que será utilizada mais a frente
    lista = []
    
    if request.method == 'POST':
        #Uso o grupo para saber a franquia do usuário
        grupos = request.user.groups.all()
        for grupo in grupos:
              a = grupo
        context['grupo'] = a
        
        #Lista contendo todas as franquias de acordo com o grupo
        lista = list(Franquia.objects.all().filter(franquia_descricao = a))
        
        #O colaborador é procurado de acordo com o filtro utilizado, utilizando sempre a primeira franquia encontrada na lista de franquias
        var = Colaborador.objects.search(request.POST.get('colaborador_nome')).filter(colaborador_franquia = lista[0])
        
        context['controle'] = 1 #Controle para template 
        context['form'] = var #contexto com os colaboradores encontrados
        return render(request,'mibcolaboradores/consultar.html', context)
    else:
        #Senão for post é exibido formulário de consulta
        var = ColaboradorForm()
        context['form'] = var
        return render(request, 'mibcolaboradores/consultar.html',context)

@login_required
def editar(request, pk):#Recebe a pk na solicitação da url
    context = {}
    var = get_object_or_404(Colaborador, pk=pk)#Pego no BD o colaborador específico
    franquia_old = var.colaborador_franquia
    if request.method == "POST":#Se verdadeiro significa que o colaborador já foi editado e então precisa ser salvo
        form = ColaboradorForm(request.POST, instance = var)#form recebe o formulário com as edições
        if form.is_valid():#Verifica se o formulário é válido
            colaborador = form.save(commit = False)#Não salva ainda
            
            ##Uso o grupo para saber a franquia do usuário
            grupos = request.user.groups.all()
            for grupo in grupos:
                a = str(grupo)
            
            #Pego a primeira franquia encontrada de acordo com o grupo do usuário e adiciono ao usuário    
            for franquia in Franquia.objects.all():
                if franquia.franquia_descricao == a:
                    colaborador.colaborador_franquia = franquia
                    if str(franquia_old) != str(franquia.franquia_descricao):
                        form.send_mail(colaborador)
                    break
            
            #Se o colaborador for editado para demitido é enviado email para os responsáveis
            if colaborador.colaborador_demissao:
                form.send_mail(colaborador)
            colaborador.save()#Salvo o colaborador
            context['controle'] = 2 #Controle para o template saber se vai consultar ou exibir uma mensagem de êxito da última alteração
            return render(request, 'mibcolaboradores/consultar.html', context)
        else:
            context['form'] = form
            return render(request, 'mibcolaboradores/editar.html', context)
    else:
        form = ColaboradorForm(instance = var)#Se falso a página é aberta com os dados do colaborador	
        return render(request, 'mibcolaboradores/editar.html', {'form': form})

@login_required
def transferir(request):
    context = {}
    context['controle'] = 0
    if request.method == "POST":
        franquia = request.POST.get('franquia')
        
        #Lista contendo todas as franquias de acordo com o grupo
        lista = list(Franquia.objects.all().filter(franquia_descricao = franquia))

        #O colaborador é procurado de acordo com o filtro utilizado, utilizando sempre a primeira franquia encontrada na lista de franquias
        var = Colaborador.objects.filter(colaborador_franquia = lista[0]).filter(colaborador_ativo = False)
        if var:
            context['controle'] = 1
        else:
            context['controle'] = 2
        context['franquia'] = franquia
        context['form'] = var
        return render(request, 'mibcolaboradores/transferir.html', context)
        
    return render(request, 'mibcolaboradores/transferir.html', context)
    
@login_required
def administrativo(request):
    context = {}
    if request.user.is_staff:
        context['usuario'] = request.user
        context['colaboradores'] = Colaborador.objects.all().filter(colaborador_ativo = True)
        context['franquias'] = Franquia.objects.all()
        #context['franquias'] = Group.objects.all()
        #context['json'] = serializers.serialize("json",Colaborador.objects.all())
        return render(request,'mibcolaboradores/administrativo.html', context)
    return redirect('login')

@login_required
def erro(request):
    return render(request, 'mibcolaboradores/erro.html')