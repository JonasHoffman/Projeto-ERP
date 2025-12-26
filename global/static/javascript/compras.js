document.addEventListener("DOMContentLoaded", function () {
    const addBtn = document.querySelector(".add-item-antecipacao");
    if (!addBtn) return;

    addBtn.addEventListener("click", function () {

        const totalForms = document.querySelector("[id$='-TOTAL_FORMS']");
        if (!totalForms) {
            alert("management_form não encontrado");
            return;
        }

        let index = parseInt(totalForms.value);

        const emptyForm = document.getElementById("form-vazio");
        const newRow = emptyForm.cloneNode(true);

        newRow.removeAttribute("id");
        newRow.style.display = "";

        newRow.querySelectorAll("input, select").forEach((el) => {
            el.name = el.name.replace("__prefix__", index);
            el.id = el.id.replace("__prefix__", index);
            el.value = "";
        });

        document.getElementById("tabela-itens").appendChild(newRow);

        totalForms.value = index + 1;
    });
});


function abrirModalAntecipacao() {
    const btn = document.getElementById("btnAbrirAntecipacao");

    // valor total vindo do template
    const total = parseFloat(btn.dataset.valor);

    // abre modal
    document.getElementById("modalAntecipacao").style.display = "block";

    // deixa TOTAL selecionado
    document.querySelector('input[name="tipo"][value="total"]').checked = true;

    // coloca o valor total no input
    const campoValor = document.getElementById("valorAntecipacao");
    campoValor.value = total.toFixed(2);
}

function preencherValor() {
    const btn = document.getElementById("btnAbrirAntecipacao");
    const total = parseFloat(btn.dataset.valor);
    document.getElementById("valorAntecipacao").value = total.toFixed(2);
}

function limparValor() {
    document.getElementById("valorAntecipacao").value = "";
}

function fecharModal() {
    document.getElementById("modalAntecipacao").style.display = "none";
}

