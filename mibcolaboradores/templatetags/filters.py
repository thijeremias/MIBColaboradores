from django import template
from django.contrib.auth.models import User, Group
from mibcolaboradores.models import Franquia

register = template.Library()
#modulo para contar os colaboradores por função e retornar ao template
@register.filter
def car(colaboradores,funcao):
    utilizados = 0
    for colaborador in colaboradores:
        if colaborador.colaborador_funcao == funcao and colaborador.colaborador_demissao is None:
            utilizados += 1
    return utilizados
    
@register.filter  
def filtra(colaboradores,franquia):
    for cont in Franquia.objects.all():
        if cont.franquia_descricao == franquia.franquia_descricao:
            colaboradores = colaboradores.filter(colaborador_franquia = cont)
            break
    return colaboradores