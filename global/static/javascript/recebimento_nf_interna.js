let itemSelecionado = '';
let itemSelecionadoIndex = null;   // <= AGORA USAMOS ID DO ITEM

const inputDoLoteBD = document.querySelector('[name="lote"]');
const inputNrEmbalagemBD = document.querySelector('[name="nr_embalagem"]');
const inputQtdPorCaixaBD = document.querySelector('[name="quantidade_por_caixa"]');
const content2 = document.querySelector('.content-footer-header2-base3');
const content3 = document.querySelector('.content3');
const areaLote = document.querySelector('.area-lote');
const areaform = document.querySelector('.form-recebimento-interno')
console.log('areaLote:', areaLote);

// ===============================
//  INPUT: QUANTIDADE DE CAIXA
// ===============================
const labelQtdDeCaixa = document.createElement('label');
labelQtdDeCaixa.innerText = 'Quantidade de caixa';
labelQtdDeCaixa.className = 'label-quantidade-de-caixa'
const inputQtdDeCaixa = document.createElement('input');
inputQtdDeCaixa.type = "text"
inputQtdDeCaixa.setAttribute('name', 'quantidade_de_caixa');
areaform.appendChild(labelQtdDeCaixa);
areaform.appendChild(inputQtdDeCaixa);

const selectDeposito = content2.querySelector('.select-deposito');
const labelSelectDeposito = content2.querySelector('#label-select');
areaform.appendChild(labelSelectDeposito);
areaform.appendChild(selectDeposito);


// ===============================
//     FUNÇÕES BÁSICAS
// ===============================
function nadaSelecionado() {
    if (!itemSelecionado) {
        return alert('Selecione um item');
    }
}

function preencheQuantidade(quantidade, item, index) {

    itemSelecionado = item;
    itemSelecionadoIndex = index;

    const itemSalvo = buscarItemSalvo(index);


    resetarCamposDeCalculo();
    
    if (itemSalvo) {
        carregarDadosSalvos(index);
        return;
    }

    // comportamento padrão (item novo)
    areaLote.innerHTML = '';
    inputNrEmbalagemBD.value = quantidade;
}

function checainputLote() {
    if (!inputDoLoteBD.value) return alert('Preencha o lote antes!');
}

function apenasNumeros(dado) {
    if (isNaN(Number(dado))) alert('Digite apenas números');
}


// ===============================
//     EVENTOS DOS INPUTS
// ===============================
inputQtdPorCaixaBD.addEventListener('change', (e) => {
    nadaSelecionado();
    apenasNumeros(inputQtdPorCaixaBD.value);
    checainputLote();
    divideQtdDeEmbalagens(inputQtdPorCaixaBD.value, e.target.name);
});

inputQtdDeCaixa.addEventListener('change', (e) => {
    nadaSelecionado();
    apenasNumeros(inputQtdPorCaixaBD.value);
    checainputLote();
    divideQtdDeEmbalagens(inputQtdDeCaixa.value, e.target.name);
});


// ===============================
//  FUNÇÃO QUE DESENHA OS LOTES
// ===============================
function divideQtdDeEmbalagens(quantidade, chamou) {

    if (!quantidade || Number(quantidade) === 0) return;

    areaLote.innerHTML = '';

    const containerLote = document.createElement('div');
    const containerEmbalagem = document.createElement('div');

    containerLote.classList.add('container-lote');
    containerEmbalagem.classList.add('container-embalagem');

    areaLote.appendChild(containerLote);
    areaLote.appendChild(containerEmbalagem);

    let conta = Number(inputNrEmbalagemBD.value) / Number(quantidade);
    if (chamou === 'quantidade_de_caixa' && conta % 1 === 0) {
        conta = quantidade;
    }

    if (conta % 1 === 0) {
        // quantidade exata
        for (let i = 0; i < conta; i++) {
            criaLinha(containerLote, containerEmbalagem, i, quantidade, chamou);
        }
    } else {
        // com resto
        let total = Math.floor(conta) + 1;

        if (chamou === 'quantidade_de_caixa') total = quantidade;

        for (let i = 0; i < total; i++) {
            criaLinha(containerLote, containerEmbalagem, i, quantidade, chamou, total);
        }
    }
}


// ===============================
//      FUNÇÃO AUXILIAR (LINHA)
// ===============================
function criaLinha(containerLote, containerEmbalagem, i, quantidade, chamou, total = null) {

    const divLote = document.createElement('div');
    divLote.classList.add('div-lote');
    const divEmbalagem = document.createElement('div');
    divEmbalagem.classList.add('div-embalagem');

    containerLote.appendChild(divLote);
    containerEmbalagem.appendChild(divEmbalagem);

    const labelLote = document.createElement('label');
    labelLote.innerText = 'Lotes - ';
    const inputLote = document.createElement('input');
    inputLote.classList.add('input-lote');
    inputLote.value = `Lote ${inputDoLoteBD.value} ${i + 1}`;

    const labelEmbalagem = document.createElement('label');
    labelEmbalagem.innerText = 'Quantidade - ';
    const inputEmbalagem = document.createElement('input');
    inputEmbalagem.classList.add('input-embalagem');

    divLote.appendChild(labelLote);
    divLote.appendChild(inputLote);
    divEmbalagem.appendChild(labelEmbalagem);
    divEmbalagem.appendChild(inputEmbalagem);

    if (!total || i + 1 < total) {
        // normal
        if (chamou === 'quantidade_de_caixa') {
            inputEmbalagem.value = Math.floor(Number(inputNrEmbalagemBD.value) / quantidade);
        } else {
            inputEmbalagem.value = quantidade;
        }
        return;
    }

    // último item (resto)
    if (chamou === 'quantidade_de_caixa') {
        let cada = Math.floor(Number(inputNrEmbalagemBD.value) / quantidade);
        let resto = Number(inputNrEmbalagemBD.value) - ((quantidade - 1) * cada);
        inputEmbalagem.value = resto;
    } else {
        let cada = Math.floor(Number(inputNrEmbalagemBD.value) / quantidade);
        let resto = Number(inputNrEmbalagemBD.value) - (quantidade * cada);
        inputEmbalagem.value = resto;
    }
}


// ===============================
//  🔵 LISTA DE ITENS DA NF
// ===============================
const itensNF = JSON.parse(document.getElementById('nomes_itens_js').textContent);


// ===============================
// BOTÃO SALVAR ITEM
// ===============================
const botaoSalvar = document.querySelector('#salvar');
botaoSalvar.addEventListener('click', () => {
    salvarDados();
    verificaItensSalvos();
});


// ===============================
// SALVAR NO SESSION STORAGE (CORRIGIDO)
// ===============================
function salvarDados() {

    const lotes = [];
    const embalagem = [];

    document.querySelectorAll('.div-lote').forEach(div => {
        lotes.push({ lote: div.querySelector('.input-lote').value });
    });

    document.querySelectorAll('.div-embalagem').forEach(div => {
        embalagem.push({ qtdEmbalagem: div.querySelector('.input-embalagem').value });
    });

    const dadosParaEnviar = {
        id_item_nf: itemSelecionadoIndex,    // <= SALVO COM ID ÚNICO
        nome_produto: itemSelecionado,
        lote: lotes,
        nr_embalagem: embalagem,
        deposito: document.querySelector('.select-deposito').value
    };

    let itensSalvos = JSON.parse(sessionStorage.getItem('itensSalvos')) || [];

    // remover item anterior se já existir o mesmo ID
    itensSalvos = itensSalvos.filter(obj => obj.id_item_nf !== itemSelecionadoIndex);

    itensSalvos.push(dadosParaEnviar);

    sessionStorage.setItem('itensSalvos', JSON.stringify(itensSalvos));
}


// ===============================
// VERIFICA SE TODOS FORAM SALVOS
// ===============================
function verificaItensSalvos() {
    const itensSalvos = JSON.parse(sessionStorage.getItem('itensSalvos')) || [];
    if (itensSalvos.length === itensNF.length) {
        document.querySelector("#enviar-form").style.display = 'block';
    }
}


// ===============================
// ENVIO PARA DJANGO
// ===============================
document.querySelector("#enviar-form").addEventListener('click', e => {
    e.preventDefault();
    enviarParaDjango();
});


function enviarParaDjango() {
    const campoNF = document.querySelector('#NF').textContent.trim();
    const dados = JSON.parse(sessionStorage.getItem('itensSalvos') || '[]');
    
    // Agora enviamos o NUMERO DO PEDIDO (ex: "PC-0118")
    const pedidoNumero = document.querySelector('#numero_pedido').value.trim();

    console.log('NF:', campoNF);
    console.log('Pedido (numero):', pedidoNumero);
    console.log('Dados enviados:', dados);

 fetch(`/estoque/recebimento_nf_interna/${campoNF}`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
        itens: dados,
        pedido_numero: pedidoNumero
    })
})
.then(response => {
    if (!response.ok) {
        throw new Error('Erro HTTP: ' + response.status);
    }
    return response.json();
})
.then(data => {

    if (data.erro) {
        alert("ERRO: " + data.erro);
        return;
    }

    // ✅ LIMPA A SESSÃO
    sessionStorage.removeItem('itensSalvos');

    // limpa visual
    areaLote.innerHTML = '';
    document.querySelector("#enviar-form").style.display = 'none';

    alert('Dados salvos com sucesso!');
    window.location.href = '/financeiro/conta/pagamento/'
})
.catch(err => {
    console.error('Erro no fetch:', err);
    alert('Erro ao gravar os dados. Verifique o console.');
});
}


// ---------- GET COOKIE (CSRF) ----------
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie) {
        const cookies = document.cookie.split(';');
        for (const c of cookies) {
            const cookie = c.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
            }
        }
    }
    return cookieValue;
}


// ---------- ABRIR LISTA DE PEDIDOS ----------
function abrirListaPedidos() {
    window.open("/compras/compras/selecionar", "_blank");
}

function buscarItemSalvo(itemId) {
    const itensSalvos = JSON.parse(sessionStorage.getItem('itensSalvos')) || [];
    return itensSalvos.find(obj => obj.id_item_nf === itemId);
}

function carregarDadosSalvos(itemId) {

    const item = buscarItemSalvo(itemId);
    if (!item) return; // ainda não foi salvo

    // limpa área de lotes
    areaLote.innerHTML = '';

    // seleciona item atual
    itemSelecionadoIndex = item.id_item_nf;
    itemSelecionado = item.nome_produto;

    // depósito
    document.querySelector('.select-deposito').value = item.deposito;

    // quantidade total (soma das embalagens)
    const total = item.nr_embalagem.reduce(
        (acc, e) => acc + Number(e.qtdEmbalagem),
        0
    );

    inputNrEmbalagemBD.value = total;

    // cria containers
    const containerLote = document.createElement('div');
    const containerEmbalagem = document.createElement('div');

    containerLote.classList.add('container-lote');
    containerEmbalagem.classList.add('container-embalagem');

    areaLote.appendChild(containerLote);
    areaLote.appendChild(containerEmbalagem);

    // recria linhas exatamente como estavam
    item.lote.forEach((l, i) => {

        const divLote = document.createElement('div');
        divLote.classList.add('div-lote');

        const inputLote = document.createElement('input');
        inputLote.classList.add('input-lote');
        inputLote.value = l.lote;

        divLote.appendChild(document.createTextNode('Lotes - '));
        divLote.appendChild(inputLote);

        containerLote.appendChild(divLote);

        const divEmb = document.createElement('div');
        divEmb.classList.add('div-embalagem');

        const inputEmb = document.createElement('input');
        inputEmb.classList.add('input-embalagem');
        inputEmb.value = item.nr_embalagem[i].qtdEmbalagem;

        divEmb.appendChild(document.createTextNode('Quantidade - '));
        divEmb.appendChild(inputEmb);

        containerEmbalagem.appendChild(divEmb);
    });
}

function resetarCamposDeCalculo() {
    inputQtdDeCaixa.value = '';
    inputQtdPorCaixaBD.value = '';
}