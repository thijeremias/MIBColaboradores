from django.contrib import admin
from .models import Funcao, Franquia, Colaborador

class FuncaoAdmin(admin.ModelAdmin):#Classe para adicionar seu modelo ao admin
    model = Funcao 
    list_display = ['funcao_descricao'] #Campos que aparecerão na lista de visualização no admin
    list_filter = ['funcao_descricao']  #Campos que serão usados como filtro no admin
    search_fields = ['funcao_descricao']#Campos que serão usados para busca no admin
    save_on_top = True #Especifica que a opção de salvar será exibida na parte de cima e debaixo da tela no admin
    
admin.site.register(Funcao, FuncaoAdmin) #Faz o resgistro do modelo no admin
#Restante segue como o primeiro
class FranquiaAdmin(admin.ModelAdmin):
    model = Franquia
    list_display = ['franquia_descricao', 'franquia_funcao', 'franquia_limite']
    list_filter = ['franquia_descricao', 'franquia_funcao']
    search_fields = ['franquia_descricao', 'franquia_funcao']
    save_on_top = True
    
admin.site.register(Franquia, FranquiaAdmin)

class ColaboradorAdmin(admin.ModelAdmin):
    model = Colaborador
    list_display = ['colaborador_nome', 'colaborador_franquia', 'colaborador_funcao']
    list_filter = ['colaborador_franquia', 'colaborador_funcao', 'colaborador_ativo']
    search_fields = ['colaborador_nome', 'colaborador_cpf']
    save_on_top = True
    
admin.site.register(Colaborador, ColaboradorAdmin)