Seção 1 — Diagnóstico
 
 PROBLEMA 1: Endpoint de consulta de pedidos demora 8–12 segundos em horário de pico. 
 
  Causa raiz, Consultas SQL sem índices apropriados, possivelmente joins entre muitas tabelas (pedidos, clientes, produtos, pagamentos) e falta de cache

  Risco técnico	Banco de dados sobrecarregado, timeout de conexões, degradação geral do sistema
 
  Risco de negócio	Clientes desistem da compra, abrem chamados no suporte, impacto na receita

  Matriz Eisenhower	URGENTE e IMPORTANTE (afeta clientes agora, perda de vendas imediata)

 PROBLEMA 2: Dois pedidos foram criados em duplicidade na última semana.

  Causa raiz	Falta de idempotência no endpoint de criação; usuário clicou duas vezes no botão "finalizar compra" ou houve retry automático

  Risco técnico	Inconsistência de dados, estoque sendo debitado duas vezes

  Risco de negócio	Cliente é cobrado duas vezes, insatisfação, chargeback, prejuízo financeiro

  Matriz Eisenhower	URGENTE e IMPORTANTE (impacta financeiro diretamente, risco alto)

 PROBLEMA 3: Bug de cálculo de frete foi corrigido em produção diretamente (sem PR, sem teste)

  Causa raiz	Ausência de processo de deploy definido; cultura de "apagar incêndio" sem revisão

  Risco técnico	Correção pode introduzir outro bug; sem PR ninguém revisa; sem teste, ninguém valida

  Risco de negócio	Próxima correção pode quebrar produção em horário de pico, parando o sistema

  Matriz Eisenhower	IMPORTANTE, mas NÃO URGENTE (o risco é alto, mas não está causando problema neste momento)

 PROBLEMA 4: Código da camada de negócio tem +4.000 linhas em um único arquivo
 
 Causa raiz	Crescimento orgânico sem refatoração; ninguém separou responsabilidades ao longo de 5 anos

 Risco técnico	Dificuldade para entender, testar e modificar; alto risco de introduzir bugs

 Risco de negócio	Atraso na entrega de novas funcionalidades; bugs demoram para ser resolvidos

 Matriz Eisenhower	IMPORTANTE, mas NÃO URGENTE (prejudica produtividade, mas não afeta cliente diretamente agora)

 PROBLEMA 5: Não há testes automatizados

 Causa raiz	Time nunca priorizou qualidade; pressão por entregas rápidas; cultura de "funcionou na minha máquina"

 Risco técnico	Cada alteração pode quebrar funcionalidades existentes sem ninguém saber

 Risco de negócio	Sistema instável; correções de emergência recorrentes; confiança do cliente abalada

 Matriz Eisenhower	IMPORTANTE, mas NÃO URGENTE (fundamental para saúde do sistema, mas não é um incêndio agora)


Seção 2 — Plano de Ação
 
 Problemas priorizados:
 
 1-Pedidos duplicados(P2)

 2-Consultas lentas(P1)

 3-Sem testes autorizados(P5)

 PROBLEMA 1
 Pedidos sendo criados duas vezes (cliente clica duas vezes ou sistema faz retry)
 
 Adicionar um campo idempotency_key no cabeçalho da requisição (enviado pelo frontend)
 
 Criar uma tabela/estrutura para armazenar chaves já processadas com seus respectivos resultados

 No endpoint de criação:

 Verificar se a chave já existe no banco

 Se existir retornar a resposta salva anteriormente (sem processar novamente)

 Se não existir processar o pedido, salvar o resultado e armazenar a chave

 Esforço estimado	8 horas (1 dia)

 Mesmo pedido enviado duas vezes com a mesma chave  segunda requisição retorna sucesso sem criar duplicata; zero pedidos duplicados em 30 dias

 PROBLEMA 2
 Melhorar performance da consulta de pedidos Consulta de pedidos demorando 8-12 segundos em horário de pico.

 O que será feito:
 Parte 1 - Banco de dados:

 Identificar as colunas mais usadas nas cláusulas WHERE e JOIN das consultas lentas (ex: cliente_id, status, data_criacao)

 Adicionar índices nessas colunas para acelerar as buscas

 Otimizar a consulta principal para evitar o problema de N+1 (buscar dados relacionados em uma única consulta em vez de várias)

 Parte 2 - Cache:

 Implementar uma camada de cache (ex: Redis ou memória local)

 Armazenar resultados de consultas frequentes por um período curto (ex: 5 minutos)

 Invalidar o cache quando novos pedidos são criados ou atualizados

 Esforço estimado	2 dias (16 horas)

 Critério de sucesso	Tempo de resposta da consulta em horário de pico cai de 8-12s para menos de 2 segundos

 PROBLEMA 3: Implementar testes automatizados
 Nenhum teste automatizado no sistema
 

 Parte 1 - Configuração:

 Escolher e instalar um framework de teste adequado para a linguagem do projeto (ex: Jest para Node.js, Pytest para Python, JUnit para Java)

 Configurar o ambiente para rodar testes localmente e no pipeline de CI

 Parte 2 - Testes unitários:

 Identificar as regras de negócio mais críticas (cálculo de frete, criação de pedido, validações)

 Criar testes que validem essas regras isoladamente

 Cada teste deve verificar um comportamento específico (ex: "frete grátis para compras acima de R$100")

 Parte 3 - Testes de integração:

 Criar testes que chamam os endpoints principais da API

 Validar os códigos de retorno HTTP e a estrutura das respostas

 Testar cenários de erro (campos faltando, IDs inválidos)

 Parte 4 - Automação:

 Configurar o pipeline de CI (ex: GitHub Actions) para rodar os testes a cada push ou pull request

 Bloquear merges se algum teste falhar

 Esforço total estimado	3 dias (24 horas)

 Critério de sucesso	Cobertura mínima de 80% nas regras de negócio críticas; novos PRs não podem ser mesclados com testes falhando



Seção 3: Opção A — Refatoração incremental

 1. Risco é o fator mais importante
 Critério Opção A (Incremental) Opção B (Reescrita)
 Risco de quebrar produção Baixo	Muito Alto Conhecimento do código Aproveita conhecimento existente	Perde regras não documentadas.
 O sistema está em produção há 5 anos. Esse código contém regras de negócio que:
 Ninguém conhece completamente, não estão documentadas é não têm testes para validar

 Uma reescrita total (Opção B) inevitavelmente vai esquecer alguma regra, resultando em bugs em produção.

 2. Ausência de testes torna a reescrita inviável
 Situação Opção A Opção B sem testes para validar Refatoração pequena + teste manual	Reescrita enorme + impossível testar tudo
 Garantia de comportamento Alta (muda pouco por vez)	Baixa (muda tudo de uma vez). Sem testes automatizados, a Opção B é um tiro no escuro.

 3. Time ocupado precisa de entregas contínuas
 Aspecto	Opção A	Opção B
 Tempo sem entregar Zero (entregas normais continuam) Semanas/meses (reescrevendo)
 Bloqueio do time Baixo (1 dev por vez)	Alto (vários devs parados)
 Motivação do time Alta (melhorias graduais)	Baixa (trabalho invisível)
 O time já está ocupado. Uma reescrita total pararia novas funcionalidades por semanas. A refatoração incremental permite melhorar enquanto entrega.

 4. Estratégia proposta para a Opção A
 Fase O que fazer Esforço
 1	Extrair uma classe/função por vez	Contínuo
 2	Adicionar teste ANTES de mexer na parte	1-2 dias
 3	Cada PR com no máximo 100 linhas alteradas	-
 4	Fazer deploy imediatamente após cada extração	-
 Resultado após 2 meses: Código modular, com testes, sem nunca ter parado o sistema.
 
 
Seção 4 — Requisitos Não Funcionais Ignorados
 RNF 1: Desempenho
 Está comprometido porque a consulta de pedidos demora 8 a 12 segundos em horário de pico.
 Métrica proposta: Tempo de resposta P95 deve ser menor que 2 segundos.
  
  RNF 2: Confiabilidade
 Está comprometido porque pedidos estão sendo criados em duplicidade.
 Métrica proposta: Zero pedidos duplicados por mês. Menos de 0,1% de requisições com erro.

 RNF 3: Manutenibilidade
 Está comprometido porque a camada de negócio tem mais de 4.000 linhas em um único arquivo.
 Métrica proposta: Nenhum arquivo deve ultrapassar 500 linhas. Tempo para implementar nova regra deve ser menor que 4 horas.
 