### Decisões de arquitetura no backend

1. **Persistência em arquivo JSON** - Escolhi usar um arquivo JSON (`data/tasks.json`) como banco de dados porque é simples, não precisa instalar nada e atende ao tamanho do projeto.

2. **Separação em funções** - Criei funções separadas para cada responsabilidade:
   - `lerTasks()` → lê os dados do arquivo
   - `salvarTasks()` → salva os dados no arquivo
   - Cada endpoint (GET, POST, PATCH, DELETE) tem sua própria função

3. **Tratamento de erros** - Cada endpoint valida os dados e retorna códigos HTTP corretos:
   - 400 quando falta informação
   - 404 quando a tarefa não existe
   - 500 quando dá erro no servidor

4. **Sem camadas complexas** - Por ser um projeto pequeno, não criei camadas separadas (Controller, Service, Repository). Tudo está no mesmo arquivo `server.js`, mas organizado por função.

### Garantindo confiabilidade em produção

**1. Logs (Registros)**
- Registrar todas as requisições que chegam (método, URL, horário)
- Registrar erros que acontecem
- Exemplo no código: `console.log(`[${new Date().toISOString()}] ${method} ${url}`)`
- Ferramentas que ajudam: Winston, Morgan, ou serviço de log como Sentry

**2. Testes automatizados**
- Testar se cada endpoint funciona antes de subir para produção
- Testar casos de erro (título vazio, ID inválido, etc.)
- Rodar testes automaticamente a cada novo código (CI/CD)

**Outros aspectos importantes:**
- **Health Check:** Endpoint `/health` para saber se a API está viva
- **Rate Limiting:** Limitar número de requisições por usuário para evitar sobrecarga
- **Timeout:** Definir tempo máximo de resposta para não travar

### Mudanças para múltiplos usuários com autenticação

**1. Banco de dados**
- Trocar o arquivo JSON por um banco de dados real (PostgreSQL, MySQL ou SQLite)
- Criar uma tabela `usuarios` com: id, email, senha_hash
- Adicionar o campo `usuario_id` em cada tarefa para saber de quem ela é

**2. Autenticação**
- Criar endpoint `POST /auth/register` para criar conta
- Criar endpoint `POST /auth/login` para fazer login e retornar um token JWT
- O token JWT é enviado pelo usuário em todas as requisições

**3. Middleware de autenticação**
- Criar uma função que roda antes de cada endpoint
- Essa função verifica se o token é válido
- Extrai o `usuario_id` do token e passa para o endpoint

**4. Mudanças nos endpoints atuais**
- `GET /tasks` → retorna apenas tarefas do usuário logado
- `POST /tasks` → cria tarefa com o `usuario_id` do usuário logado
- `PATCH /tasks/{id}` → verifica se a tarefa pertence ao usuário antes de atualizar
- `DELETE /tasks/{id}` → verifica se a tarefa pertence ao usuário antes de deletar

**5. Segurança**
- Hash nas senhas (bcrypt)
- JWT com expiração
- HTTPS obrigatório em produção