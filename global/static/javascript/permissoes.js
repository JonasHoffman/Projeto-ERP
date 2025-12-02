const csrftoken = document.getElementById("csrf_token").value;

let alvoTipo = null;   // grupo | usuario
let alvoId = null;     // id selecionado

//---------------------------------------------------------------
// Selecionou grupo ou usuário
//---------------------------------------------------------------
function selecionarAlvo(tipo) {
    alvoTipo = tipo;

    if (tipo === "grupo") {
        alvoId = document.getElementById("select_grupo").value;
        document.getElementById("select_usuario").value = "";
    } else {
        alvoId = document.getElementById("select_usuario").value;
        document.getElementById("select_grupo").value = "";
    }

    document.getElementById("area_views").innerHTML = "";
}

//---------------------------------------------------------------
// Carregar views do módulo selecionado
//---------------------------------------------------------------
function carregarViewsModulo(moduloId) {

    if (alvoTipo === "grupo") {
        alvoId = document.getElementById("select_grupo").value;
    } else if (alvoTipo === "usuario") {
        alvoId = document.getElementById("select_usuario").value;
    }

    if (!alvoId) {
        alert("Selecione um grupo ou usuário primeiro!");
        return;
    }

    fetch(`/accounts/carregar_views/${moduloId}/?tipo=${alvoTipo}&id=${alvoId}`)
        .then(r => r.json())
        .then(data => {
            let tbody = document.getElementById("area_views");
            tbody.innerHTML = "";

            let template = document.getElementById("linha_view_template");

            data.views.forEach(v => {
                let linha = template.content.cloneNode(true);

                linha.querySelector(".col-nome").textContent = v.nome;
                linha.querySelector(".col-rota").textContent = v.rota;

                let chk = linha.querySelector(".chk-permissao");
                chk.checked = v.pode;

                chk.dataset.view = v.id;
                chk.dataset.tipo = alvoTipo;
                chk.dataset.id = alvoId;

                // Adiciona listener para salvar ao alterar
                chk.addEventListener("change", function () {
                    salvarPermissao(this);
                });

                tbody.appendChild(linha);
            });
        });
}

//---------------------------------------------------------------
// Salvar permissão
//---------------------------------------------------------------
function salvarPermissao(chk) {
    let formData = new FormData();
    formData.append("view_id", chk.dataset.view);
    formData.append("tipo", chk.dataset.tipo);
    formData.append("id", chk.dataset.id);
    formData.append("pode", chk.checked);

    fetch("/accounts/salvar_permissao/", {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": csrftoken }
    })
    .then(r => r.json())
    .then(data => {
        console.log("Permissão salva:", data);
    })
    .catch(e => console.error("Erro ao salvar permissão:", e));
}