function selecionarEmpresa() {
    var dropdown = document.getElementById("empresas");
    var empresaSelecionada = dropdown.options[dropdown.selectedIndex].text;
    console.log("Empresa selecionada:", empresaSelecionada);
}