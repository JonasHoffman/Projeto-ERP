document.addEventListener("focusout", function (e) {
    if (!e.target.classList.contains("codigo-produto")) return;
    const input = e.target;
    const codigo = input.value.trim();
    if (!codigo) return;

    const contexto = input.dataset.contexto || "";

    fetch(`/buscas/buscar-produto/?q=${encodeURIComponent(codigo)}&contexto=${contexto}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Produto não encontrado");
            }
            return response.json();
        })
        .then(data => {
            const row = input.closest("tr");

            // input visível do código
            const produtoInput = row.querySelector("input[name$='codigo_produto']");
            // hidden input que recebe o ID
            const produtoInputHidden = row.querySelector("input[type='hidden'][name$='-produto']");

            const nomeDiv = row.querySelector(".produto-nome");

            // seta ID no hidden
            produtoInputHidden.value = data.id;

            // exibe código no input visível
            produtoInput.value = data.codigo;

            // exibe código + nome
            nomeDiv.innerText = `${data.codigo} - ${data.nome}`;
            nomeDiv.classList.remove("text-danger");

            // preço automático
            const precoInput = row.querySelector("input[name$='valor_unitario']");
            if (precoInput && !precoInput.value && data.preco !== undefined) {
                precoInput.value = Number(data.preco).toFixed(2);
            }

            // estoque
            const estoqueDiv = row.querySelector(".produto-estoque");
            if (estoqueDiv && data.estoque !== undefined) {
                estoqueDiv.innerText = `Estoque: ${data.estoque}`;
            }
        })
        .catch(() => {
            const row = input.closest("tr");

            // limpa apenas o hidden
            const produtoInputHidden = row.querySelector("input[type='hidden'][name$='-produto']");
            produtoInputHidden.value = "";

            const nomeDiv = row.querySelector(".produto-nome");
            nomeDiv.innerText = "Produto não encontrado";
            nomeDiv.classList.add("text-danger");
        });
});
