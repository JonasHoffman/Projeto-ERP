let campoNome = null;
let campoId = null;

function abrirModalBusca(url, titulo, inputNome, inputId) {
    campoNome = inputNome;
    campoId = inputId;

    document.getElementById("titulo-modal").innerText = titulo;

    fetch(url)
        .then(r => r.text())
        .then(html => {
            document.getElementById("conteudoResultados").innerHTML = html;
            document.getElementById("modal-busca").style.display = "flex";
        });
}

function selecionarItem(id, nome) {
    document.getElementById(campoNome).value = nome;
    document.getElementById(campoId).value = id;

    fecharModalBusca();
}

function fecharModalBusca() {
    document.getElementById("modal-busca").style.display = "none";
}