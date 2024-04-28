function selecionarEmpresa() {
    var dropdown = document.getElementById("empresas");
    var empresaSelecionada = dropdown.options[dropdown.selectedIndex].text;
    console.log("Empresa selecionada:", empresaSelecionada);
}


function listarEmpresas(){
    var listaEmpresas = [
        {empresa: "Tijuquinha", id: 2},
        {empresa: "Graças", id: 3},
        {empresa: "Sãen Pena, SJC", id: 4}
    ];

    var selectEmpresas = document.getElementById("empresas");

    listaEmpresas.forEach(function(empresa)
    {
        var option = document.createElement("option");
        option.value = empresa.id;
        option.text = empresa.empresa;

        selectEmpresas.appendChild(option);
    });
}


