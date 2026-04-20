const API_URL = 'http://localhost:3000/tasks';
let filtroAtual = 'todas';

async function buscarTarefas() {
    try {
        let url = API_URL;
        if (filtroAtual !== 'todas') {
            url = `${API_URL}?status=${filtroAtual}`;
        }
        const resposta = await fetch(url);
        const dados = await resposta.json();
        return dados.tasks || [];
    } catch (error) {
        console.error('Erro:', error);
        return [];
    }
}

async function criarTarefa(titulo, prioridade) {
    const resposta = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ titulo, prioridade: parseInt(prioridade) })
    });
    return resposta.json();
}

async function atualizarTarefa(id, situacao) {
    const resposta = await fetch(`${API_URL}/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ situacao })
    });
    return resposta.json();
}

async function deletarTarefa(id) {
    await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
}

function getPrioridadeTexto(prioridade) {
    const textos = { 1: 'Alta', 2: 'Média', 3: 'Baixa' };
    return textos[prioridade];
}

function renderizarTarefas(tarefas) {
    const container = document.getElementById('listaTarefas');
    if (!tarefas.length) {
        container.innerHTML = '<p class="sem-tarefas">📭 Nenhuma tarefa encontrada</p>';
        return;
    }
    container.innerHTML = tarefas.map(t => `
        <div class="tarefa" style="border-left-color: ${t.prioridade === 1 ? '#ff4757' : t.prioridade === 2 ? '#ffa502' : '#2ed573'}">
            <div class="tarefa-info">
                <span class="tarefa-titulo ${t.situacao === 'concluida' ? 'concluida' : ''}">${t.titulo}</span>
                <span class="tarefa-prioridade prioridade-${t.prioridade}">${getPrioridadeTexto(t.prioridade)}</span>
            </div>
            <div class="tarefa-botoes">
                ${t.situacao === 'pendente' 
                    ? `<button class="btn-concluir" onclick="marcarConcluida(${t.id})">✓ Concluir</button>`
                    : `<button class="btn-concluir" onclick="marcarPendente(${t.id})" style="background:#ffa502">↩ Reabrir</button>`
                }
                <button class="btn-deletar" onclick="deletarTarefaClick(${t.id})">🗑 Excluir</button>
            </div>
        </div>
    `).join('');
}

async function carregarTudo() {
    const tarefas = await buscarTarefas();
    renderizarTarefas(tarefas);
}

async function marcarConcluida(id) {
    await atualizarTarefa(id, 'concluida');
    await carregarTudo();
}

async function marcarPendente(id) {
    await atualizarTarefa(id, 'pendente');
    await carregarTudo();
}

async function deletarTarefaClick(id) {
    if (confirm('Tem certeza?')) {
        await deletarTarefa(id);
        await carregarTudo();
    }
}

document.getElementById('criarBtn').addEventListener('click', async () => {
    const titulo = document.getElementById('tituloInput').value.trim();
    const prioridade = document.getElementById('prioridadeSelect').value;
    if (!titulo) return alert('Digite uma tarefa!');
    await criarTarefa(titulo, prioridade);
    document.getElementById('tituloInput').value = '';
    await carregarTudo();
});

document.getElementById('tituloInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') document.getElementById('criarBtn').click();
});

document.querySelectorAll('.filtro-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.filtro-btn').forEach(b => b.classList.remove('ativo'));
        btn.classList.add('ativo');
        filtroAtual = btn.getAttribute('data-filtro');
        carregarTudo();
    });
});

carregarTudo();