Ambiguidade/Falta - O que exatamente é "situação" da tarefa?
  
 PERGUNTA AO CLIENTE
  "A situação se refere apenas a 'pendente' e 'concluída', ou existem outros estados como 'em andamento' ou 'cancelada'?"

  Assumi que a situação tem apenas dois estados: pendente e concluída. É o mínimo necessário para os filtros pedidos.



Ambiguidade/Falta - Como a prioridade seria representada? Se existir uma métrica para prioridades 
 
 PERGUNTA AO CLIENTE
  "A prioridade seria um nível simples (ex: ALTA, MÉDIA, BAIXA) ou um número (ex: 1 a 3)?

  Assumi que, se implementada, a prioridade seria um campo numérico de 1 (mais alta) a 3 (mais baixa) e ordenaria as tarefas por prioridade primeiro, depois por data de criação.



Ambiguidade/Falta - As tarefas precisam ser salvas e abertas a qualquer momento do dia?

 PERGUNTA AO CLIENTE
  "As tarefas devem ser salvas em um banco de dados ou podem ficar apenas em memória (perdem ao fechar)?"

  Assumi que sim, precisam ser persistidas. Usei um arquivo JSON local para simular um banco de dados, evitando a complexidade de um SGBD completo.


Ambiguidade/Falta - Qual a ordem padrão de exibição das tarefas?

 PERGUNTA AO CLIENTE
 "As tarefas devem aparecer por ordem de criação (mais recentes primeiro), por título ou por prioridade?"

 Assumi que, a ordem de criação (mais antigas primeiro ou mais recentes), com a possibilidade de ordenar por prioridade se o requisito for implementado.



REQUISITOS FUCIONAIS (RF)
 RF01 - Listar tarefas - O sistema deve exibir todas as tarefas cadastradas em uma lista.
 
 RF02 - Criar tarefa - O sistema deve permitir a criação de uma nova tarefa com título obrigatório.
 
 RF03 - Marcar como concluída - O sistema deve permitir alterar a situação de uma tarefa de "pendente" para "concluída".
 
 RF04 - Desmarcar tarefa - O sistema deve permitir reverter uma tarefa de "concluída" para "pendente".
 
 RF05 - Deletar tarefa - O sistema deve permitir remover permanentemente uma tarefa.
 
 RF06 - Filtrar por situação - O sistema deve oferecer filtros para exibir: "Todas", "Apenas pendentes" ou "Apenas concluídas".
 
 RF09 - Prioridade (opcional) - O sistema deve permitir definir um nível de prioridade (1 a 3) para cada tarefa.
 
 RF10 - Ordenar por prioridade - O sistema deve ordenar as tarefas por prioridade (mais alta primeiro) quando o campo prioridade for implementado.




Requisitos Não Funcionais (RNF)

 RNF01	Usabilidade	A interface deve ser simples e intuitiva, com botões claros para cada ação (criar, concluir, deletar).
 
 RNF02	Persistência	Os dados devem ser salvos localmente (JSON ou localStorage) para não serem perdidos ao fechar a aplicação.
 
 RNF03	Responsividade	A interface deve se adaptar a diferentes tamanhos de tela (mobile, tablet, desktop).
 
 RNF04	Performance	A lista deve carregar e filtrar em menos de 1 segundo para até 1000 tarefas.
 
 RNF05	Manutenibilidade	O código deve ser organizado em componentes reutilizáveis (React).



Tratamento do Requisito de Prioridade no Backlog

 OBRIGATORIO (MUST): Requisitos Fucionais (RF) do RF01 ao RF03 é RF05 ao RF06 é o Requisito Não Fucional RNF02.
 
 PRIORIDADE MÉDIA(SHOULD): Requisitos Fucionais: RF04, RF09, RF10 Requisitos Não Fucionais do RNF01 ao RNF03.
 
 PRIORIDADE BAIXA(COULD): Coisas como Editar, Data vencimento, Busca, Performance, Dark mode
 
 PARA O FUTURO(WON'T): Coisas como Compartilhar tarefas, Notificações, Categorias.


