const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

const tasksFile = path.join(__dirname, 'data', 'tasks.json');

function lerTasks() {
    try {
        const dados = fs.readFileSync(tasksFile, 'utf8');
        return JSON.parse(dados);
    } catch (error) {
        return [];
    }
}

function salvarTasks(tasks) {
    fs.writeFileSync(tasksFile, JSON.stringify(tasks, null, 2), 'utf8');
}

app.get('/tasks', (req, res) => {
    const { status } = req.query;
    let tasks = lerTasks();
    
    if (status && (status === 'pendente' || status === 'concluida')) {
        tasks = tasks.filter(task => task.situacao === status);
    }
    
    tasks.sort((a, b) => {
        if (a.prioridade !== b.prioridade) return a.prioridade - b.prioridade;
        return new Date(a.criada_em) - new Date(b.criada_em);
    });
    
    res.json({ success: true, count: tasks.length, tasks });
});

app.post('/tasks', (req, res) => {
    const { titulo, prioridade = 2 } = req.body;
    
    if (!titulo || titulo.trim() === '') {
        return res.status(400).json({ success: false, error: 'Título é obrigatório' });
    }
    
    const tasks = lerTasks();
    const novaTask = {
        id: Date.now(),
        titulo: titulo.trim(),
        situacao: 'pendente',
        prioridade: prioridade,
        criada_em: new Date().toISOString()
    };
    
    tasks.push(novaTask);
    salvarTasks(tasks);
    
    res.status(201).json({ success: true, task: novaTask });
});

app.patch('/tasks/:id', (req, res) => {
    const { id } = req.params;
    const { situacao, titulo, prioridade } = req.body;
    
    const tasks = lerTasks();
    const taskIndex = tasks.findIndex(task => task.id == id);
    
    if (taskIndex === -1) {
        return res.status(404).json({ success: false, error: 'Tarefa não encontrada' });
    }
    
    if (situacao) tasks[taskIndex].situacao = situacao;
    if (titulo) tasks[taskIndex].titulo = titulo;
    if (prioridade) tasks[taskIndex].prioridade = prioridade;
    tasks[taskIndex].atualizada_em = new Date().toISOString();
    
    salvarTasks(tasks);
    res.json({ success: true, task: tasks[taskIndex] });
});

app.delete('/tasks/:id', (req, res) => {
    const { id } = req.params;
    const tasks = lerTasks();
    const taskIndex = tasks.findIndex(task => task.id == id);
    
    if (taskIndex === -1) {
        return res.status(404).json({ success: false, error: 'Tarefa não encontrada' });
    }
    
    const taskRemovida = tasks[taskIndex];
    tasks.splice(taskIndex, 1);
    salvarTasks(tasks);
    
    res.json({ success: true, message: 'Tarefa removida', task: taskRemovida });
});

app.listen(PORT, () => {
    console.log(`API rodando em http://localhost:${PORT}`);
});