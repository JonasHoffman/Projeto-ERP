document.addEventListener("DOMContentLoaded", function() {

    // ===============================
    // Função genérica para preencher hidden + input
    // ===============================
    function preencherItem(tipo, id, nome) {
        document.getElementById(`${tipo}_id`).value = id;
        document.getElementById(`${tipo}_input`).value = nome;
    }

    // ===============================
    // Verifica item digitado ao sair do input
    // ===============================
    function verificarItemAoSair(inputId, hiddenId, url, tipo) {
        const input = document.getElementById(inputId);
        input.addEventListener('blur', async () => {
            const valor = input.value.trim();
            if (!valor) {
                document.getElementById(hiddenId).value = '';
                return;
            }

            try {
                const response = await fetch(`${url}?q=${encodeURIComponent(valor)}`);
                const html = await response.text();
                const div = document.createElement('div');
                div.innerHTML = html;

                const primeiroItem = div.querySelector('.result-item');
                if (primeiroItem) {
                    const id = primeiroItem.getAttribute('data-id');
                    const nome = primeiroItem.getAttribute('data-nome');
                    preencherItem(tipo, id, nome);
                } else {
                    document.getElementById(hiddenId).value = '';
                }

            } catch (err) {
                console.error(err);
            }
        });
    }

    // ===============================
    // Inicializa verificação de Banco e Transportadora
    // ===============================
    verificarItemAoSair(
        'transportadora_input',
        'transportadora_id',
        document.getElementById('btn-transportadora').dataset.url,
        'transportadora'
    );

    verificarItemAoSair(
        'banco_input',
        'banco_id',
        document.getElementById('btn-banco').dataset.url,
        'banco'
    );

    // ===============================
    // Botões de popup
    // ===============================
    function abrirPopup(url, nomePopup) {
        window.open(url, nomePopup, "width=600,height=400,resizable=yes,scrollbars=yes");
    }

    document.getElementById("btn-transportadora").addEventListener("click", () => {
        abrirPopup(document.getElementById("btn-transportadora").dataset.url, "popupTransportadora");
    });

    document.getElementById("btn-banco").addEventListener("click", () => {
        abrirPopup(document.getElementById("btn-banco").dataset.url, "popupBanco");
    });

    // ===============================
    // Funções para preencher via popup
    // ===============================
    window.preencherTransportadora = function(id, nome) {
        preencherItem('transportadora', id, nome);
    }

    window.preencherBanco = function(id, nome) {
        preencherItem('banco', id, nome);
    }

    // ===============================
    // Formsets Dinâmicos
    // ===============================
    function addForm(prefix, templateId, containerId) {
        const total = document.getElementById(`id_${prefix}-TOTAL_FORMS`);
        const idx = total.value;
        const html = document.getElementById(templateId).innerHTML.replace(/__index__/g, idx);
        document.getElementById(containerId).insertAdjacentHTML("beforeend", html);
        total.value = parseInt(total.value) + 1;
        inicializarCEP(); // reaplica listener para novos CEPs
    }

    document.getElementById("add-endereco").addEventListener("click", () => {
        addForm("end", "endereco-template", "enderecos-container");
    });

    document.getElementById("add-contato").addEventListener("click", () => {
        addForm("cont", "contato-template", "contatos-container");
    });

    // ===============================
    // CEP (ViaCEP)
    // ===============================
    function buscarCEP(inputCep) {
        const cep = inputCep.value.replace(/\D/g, '');
        if (cep.length !== 8) return;

        fetch(`https://viacep.com.br/ws/${cep}/json/`)
            .then(resp => resp.json())
            .then(data => {
                if (data.erro) return;
                const match = inputCep.id.match(/id_end-(\d+)-cep/);
                if (!match) return;
                const idx = match[1];
                const campos = {
                    logradouro: `id_end-${idx}-logradouro`,
                    bairro: `id_end-${idx}-bairro`,
                    cidade: `id_end-${idx}-cidade`,
                    estado: `id_end-${idx}-estado`
                };
                document.getElementById(campos.logradouro).value = data.logradouro || '';
                document.getElementById(campos.bairro).value = data.bairro || '';
                document.getElementById(campos.cidade).value = data.localidade || '';
                document.getElementById(campos.estado).value = data.uf || '';
            });
    }

    function onBlurCEP(event) { buscarCEP(event.target); }

    function inicializarCEP() {
        const cepInputs = document.querySelectorAll("#enderecos-container input[name$='-cep']");
        cepInputs.forEach(input => {
            input.removeEventListener('blur', onBlurCEP);
            input.addEventListener('blur', onBlurCEP);
        });
    }

    // Inicializa CEP existentes
    inicializarCEP();

    // Observa adições dinâmicas para reaplicar listener de CEP
    const container = document.getElementById('enderecos-container');
    if (container) {
        const observer = new MutationObserver(() => { inicializarCEP(); });
        observer.observe(container, { childList: true, subtree: true });
    }

});
