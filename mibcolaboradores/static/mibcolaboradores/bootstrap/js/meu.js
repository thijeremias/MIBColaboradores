window.onload = function (){
    verificaPagina();
    var form = document.forms;
    try {
        form["franquia"].elements[2].onclick = function () {return verificaFranquia(form["franquia"]);};
    }catch(err){}
    try{
        form["form1"].elements[1].onchange = function () {verificaFormulario(form["form1"]);};
    }
    catch(err){}
    try {
        var i;
        var butao = document.getElementsByName("post");
        for (i = 0; i < butao.length; i++){
            butao[i].onclick = function () {alert("O próximo passo é editar, ativar e salvar seu novo colaborador!");};
        }
    }
    catch(err){}
    try {
        //var p;
        //var menu = document.getElementsByTagName("li");
        var menu = document.getElementById("acimalimite");
        menu.onclick = function () {
            liberaMenus();
            this.setAttribute("class","active");
            verificaAcimaLimite();
        };
        //for (p = 0; p < menu.length; p++){
        //    menu[p].onclick = function () {
        //        liberaMenus();
        //        this.setAttribute("class","active");
        //        verificaAcimaLimite();
        //    };
        //}
        menu = document.getElementById("nolimite");
        menu.onclick = function () {
            liberaMenus();
            this.setAttribute("class","active");
            verificaNoLimite();
        };
        
        menu = document.getElementById("abaixolimite");
        menu.onclick = function () {
            liberaMenus();
            this.setAttribute("class","active");
            verificaAbaixoLimite();
        };
        
        menu = document.getElementById("overview");
        menu.onclick = function () {
            liberaMenus();
            this.setAttribute("class","active");
            verificaOverview();
        };
    }
    catch(err){}
    /*try {
        verificaQuantidades();
        //var linhas = document.getElementsByTagName("tr");
        //var select = document.getElementById("seleciona_franquias");
        //select.onchange = function(){
            //recarrega(this);
            //filtraFranquia(this,linhas);
        //};
    }catch(err){}*/
};

function verificaAcimaLimite (){
    var i;
    var linhas = document.querySelectorAll("table > tbody > tr");
    for (i = 0; i < linhas.length; i++){
        var utilizados = linhas[i].childNodes.item(7).firstChild.nodeValue;
        var limites = linhas[i].childNodes.item(5).firstChild.nodeValue;
        if (utilizados > limites){
            linhas[i].setAttribute("class","danger");
        }
}
}

function verificaNoLimite (){
    var i;
    var linhas = document.querySelectorAll("table > tbody > tr");
    for (i = 0; i < linhas.length; i++){
        var utilizados = linhas[i].childNodes.item(7).firstChild.nodeValue;
        var limites = linhas[i].childNodes.item(5).firstChild.nodeValue;
        if (utilizados == limites){
            linhas[i].setAttribute("class","warning");
        }
}
}

function verificaAbaixoLimite (){
    var i;
    var linhas = document.querySelectorAll("table > tbody > tr");
    for (i = 0; i < linhas.length; i++){
        var utilizados = linhas[i].childNodes.item(7).firstChild.nodeValue;
        var limites = linhas[i].childNodes.item(5).firstChild.nodeValue;
        if (utilizados < limites){
            linhas[i].setAttribute("class","success");
        }
}
}

function verificaOverview (){
    var i;
    var linhas = document.querySelectorAll("table > tbody > tr");
    for (i = 0; i < linhas.length; i++){
        linhas[i].setAttribute("class","linhas");
        //var utilizados = linhas[i].childNodes.item(7).firstChild.nodeValue;
        //var limites = linhas[i].childNodes.item(5).firstChild.nodeValue;
        //if (utilizados < limites){
        //    linhas[i].setAttribute("class","success");
        //}
}
}


function verificaQuantidades () {
    var i;
    var linhas = document.querySelectorAll("table > tbody > tr");
    for (i = 0; i < linhas.length; i++){
        var utilizados = linhas[i].childNodes.item(7).firstChild.nodeValue;
        var limites = linhas[i].childNodes.item(5).firstChild.nodeValue;
        if (utilizados > limites){
            linhas[i].setAttribute("class","danger");
        }
        else if (utilizados == limites){
            linhas[i].setAttribute("class","warning");
        }
        else {
            linhas[i].setAttribute("class","success");
        }
    }
    //alert(linhas[0].childNodes.item(5).firstChild.nodeValue);
    //alert(linhas[0].childNodes.item(7).firstChild.nodeValue);
}
/*function recarrega (select) {
    var i;
    var tabela = document.getElementById("corpo");
    var json = JSON.parse(window.localStorage.getItem("json"));
    alert(json[0].fields.colaborador_franquia);
    var linha = document.createElement("tr");
    tabela.appendChild(linha);
    var celula = document.createElement("td");
    linha.appendChild(celula);
    var celula2 = document.createElement("td");
    linha.appendChild(celula2);
    var texto = document.createTextNode("teste");
    celula.appendChild(texto);
    /*for (i = 0; i < json.length; i++){
        if (json[i].fields.colaborador_franquia == select.options[select.selectedIndex].value){
            var linha = document.createElement("tr");
            var texto = document.createTextNode("teste");
            linha.appendChild(texto);
        }
    }
    
}

function filtraFranquia (select,linhas){
    var i;
    for(i = 1; i < linhas.length; i++){
        if (linhas[i].childNodes.item(1).firstChild.nodeValue != select.options[select.selectedIndex].value){
            linhas[i].parentNode.removeChild(linhas[i]);
            i--;
        }
    }
}*/

function liberaMenus () {
    var ativos = document.getElementsByClassName("active");
    var i;
    for (i = 0; i < ativos.length; i++){
        ativos[i].setAttribute("class","native");
    }
}

function verificaPagina () {
    var title = document.URL;
    var pagina = document.getElementsByName("pagina");
    for (var i=0;i<pagina.length;i++){
        if(title == pagina[i]){
            pagina[i].style.color = "#eee";
            
        }
    }
}

function verificaFormulario (form){
    alert("O nome: "+form.elements[1].value+" está completo? \n Senão, por favor digite o nome completo do colaborador.");
}

function verificaFranquia (form){
    var re = /\d\d$/; 
        if (re.test(form.elements[1].value)) {
            form.elements[1].value = form.elements[1].value.replace(/\w*(\d\d$)/,"franquia$1");
            var posicao = form.elements[1].value.search(/\d\d$/);
            var f = form.elements[1].value[posicao] + form.elements[1].value[posicao+1];
            if (f > 28){
                alert("Atualmente as Lojas Mib possuem 28 franquias");
                return false;
            }
        }else{
            alert("A franquia deve ser representada por 2 dígitos \nEx: 02, ou, franquia02");
            return false;
    }
}