function selecionarEmpresa() {
    var dropdown = document.getElementById("empresas");
    var empresaSelecionada = dropdown.options[dropdown.selectedIndex].text;
    console.log("Empresa selecionada:", empresaSelecionada);
}

function atualizarSelect(selectId, listItens){
    var selectItem = document.getElementById(selectId);

    // Limpar opções existentes
    selectItem.innerHTML = '';
    
    listItens.forEach(function(item)
    {
        var option = document.createElement("option");
        option.value = item.id;
        option.text = item.text;

        selectItem.appendChild(option);
    });
}

function listarEmpresas(){
    var listaEmpresas = [
        {text: "Tijuquinha", id: 2},
        {text: "Graças", id: 3},
        {text: "Sãen Pena, SJC", id: 4}
    ];

    var selectEmpresas = document.getElementById("empresas");

    atualizarSelect("empresas", listaEmpresas)
}

// FUNÇÃO TESTE, MOKANDO DADOS.
function listarCarros(idEmpresaSelecionada) {
    var carros;
    switch (idEmpresaSelecionada) {
        case "2":
            carros = [
                {text: "20501", id:1},
                {text: "20502", id:2},
                {text: "20503", id:3}
            ]
            break;
        case "3":
            // Se o ID for 3, faça algo diferente
            carros = [
                {text: "30501", id:1},
                {text: "30502", id:2},
                {text: "30503", id:3}
            ]
            break;
        case "4":
            // Se o ID for 4, faça outra coisa
            carros = [
                {text: "40501", id:1},
                {text: "40502", id:2},
                {text: "40503", id:3}
            ]
            break;
        default:
            // Se o ID não corresponder a nenhum dos casos acima
            console.log("ID não reconhecido");
    }
    atualizarSelect("carros", carros)
    console.log(carros)
}

function modifyDisplay(ids, exibition){
    for (var i = 0; i < ids.length; i++) {
        var element = document.getElementById(ids[i]);
        if (element) {
            element.style.display = exibition; // Modifica o estilo para exibição
        }
    }
}

function atualizarParametrosGravacao(modeloEquipamento){
    var IdDisplayDvr = ["dvr_label", "dvr_select"];
    var IdDisplayCameras = ["cameras_label", "cameras_select"];

    // Verificar se o modelo de equipamento é "RaspDvr"
    if (modeloEquipamento === "RaspDvr") {
        modifyDisplay(IdDisplayDvr, "block")
        modifyDisplay(IdDisplayCameras, "block")
    } else {
        modifyDisplay(IdDisplayDvr, "none")
        modifyDisplay(IdDisplayCameras, "none")
    }
}

// Executar a função listarEmpresas() quando o DOM estiver pronto
document.addEventListener("DOMContentLoaded", function() {
        // Obtendo o nome do arquivo HTML atual
        var currentPage = window.location.pathname.split("/").pop();

        // Verificando se a página atual é gravacao.html
        if (currentPage === "gravacao.html") {
            listarEmpresas();
        }
});

