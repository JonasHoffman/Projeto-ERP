function adicionarForm(prefixo, containerId, botaoId) {
    const container = document.getElementById(containerId);
    const btnAdd = document.getElementById(botaoId);

    const totalForms = document.querySelector(`#id_${prefixo}-TOTAL_FORMS`);

    if (!totalForms) {
        console.warn(`Prefixo incorreto: id_${prefixo}-TOTAL_FORMS não encontrado.`);
        return;
    }

    btnAdd.addEventListener("click", function () {
        const total = parseInt(totalForms.value);

        const formOriginal = container.querySelector(".sub-bloco:last-child");
        const novoForm = formOriginal.cloneNode(true);

        // Atualiza índices do formset
        const regex = new RegExp(`${prefixo}-\\d+`, "g");
        novoForm.innerHTML = novoForm.innerHTML.replace(regex, `${prefixo}-${total}`);

        // Limpando campos
        novoForm.querySelectorAll("input, select, textarea").forEach(campo => campo.value = "");

        // Atualizando título
        const titulo = novoForm.querySelector("h4");
        if (titulo) {
            const textoBase = titulo.innerText.split(" ")[0]; // "Endereço" ou "Contato"
            titulo.innerText = `${textoBase} ${total + 1}`;
        }

        container.appendChild(novoForm);

        totalForms.value = total + 1;
    });
}


// Inicialização
document.addEventListener("DOMContentLoaded", function () {
    adicionarForm("enderecos", "enderecos-container", "add-endereco");
    adicionarForm("contatos", "contatos-container", "add-contato");
    // 🔥 DESCONTO POR CLIENTE
    adicionarForm("descontos", "descontos-container", "add-desconto");
});

