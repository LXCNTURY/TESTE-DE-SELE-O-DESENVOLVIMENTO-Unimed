1 - Quais foram as principais decisões de tratamento que você tomou? (ex.: o que fazer com registros órfãos, como normalizar cidades)

Registros órfãos
Decisão: Remover completamente do consolidado final.
Justificativa: Uma entrega sem pedido correspondente não pode ser associada a nenhum cliente ou pedido. Manter esses registros criaria inconsistência nos indicadores (ex: ticket médio, volume por cidade). A informação é inútil para o negócio.
O que foi feito: entregas_validas = entregas[entregas['id_pedido'].isin(pedidos['id_pedido'])]

Normalização de cidades
Decisão: Padronizar todas as variações para um nome oficial.
Justificativa: O mesmo município aparece com grafias diferentes ('São Paulo', 'sao paulo', 'SAO PAULO', 'SP'). Isso distorce a contagem de pedidos por cidade.
O que foi feito: Mapeamento manual das variações mais comuns para o nome correto. Variações não mapeadas recebem title() (primeira letra maiúscula).

Datas em formatos mistos
Decisão: Tentar múltiplos formatos automaticamente e converter para datetime.
Justificativa: Os dados vieram de sistemas diferentes com padrões distintos (DD/MM/AAAA, AAAA-MM-DD). Precisamos de um formato único para calcular atrasos.
O que foi feito: Função normalizar_data() testa formatos sequencialmente até encontrar um que funciona.

Campos nulos em colunas obrigatórias
Decisão: Para valor_total vazio → substituir por 0. Para datas vazias → manter como nulo (None).
Justificativa: Valor total zerado permite que o pedido ainda seja contabilizado, sem distorcer médias (pode ser analisado separadamente).
Data vazia significa entrega não realizada → atraso fica nulo, não atrapalha indicadores de prazo.
O que foi feito: normalizar_valor_monetario() retorna 0.0 para vazio. Datas vazias retornam None.


Valores monetários com vírgula como decimal
Decisão: Substituir vírgula por ponto antes de converter para float.
Justificativa: Python usa ponto como separador decimal. '89,90' não pode ser convertido diretamente.
O que foi feito: if ',' in valor_str and '.' not in valor_str: valor_str = valor_str.replace(',', '.')


Cálculo de atraso
Decisão: Usar dias de diferença entre data realizada e prevista. Negativo = antecipado. Nulo = não entregue.
Justificativa: Permite identificar tanto atrasos quanto entregas antecipadas. O nulo é importante para não contabilizar pedidos ainda não entregues nos percentuais.
O que foi feito: (data_realizada - data_prevista).days

////////////////////////////////////////////////////////////////////////////////////////////////////

2 - Seu pipeline é idempotente? Ou seja, rodá-lo duas vezes produz o mesmo resultado? Justifique.

O pipeline é idempotente porque toda execução começa recriando os dados de entrada do zero, aplica transformações determinísticas e sempre produz o mesmo arquivo consolidado final. Você pode rodar ele quantas vezes quiser que o resultado será sempre o mesmo. 

////////////////////////////////////////////////////////////////////////////////////////////////////

3 - Se esse pipeline fosse executado diariamente com arquivos de 10 milhões de linhas, o que você mudaria na abordagem?

Minha abordagem atual carrega tudo na memória de uma vez com pd.read_csv(). Para 10 milhões de linhas, isso vai consumir muita memória RAM (vários GBs) e pode travar o computador ou o servidor.
Outro problema é que o pipeline recria os arquivos do zero a cada execução. Com 10 milhões de linhas diárias, isso seria extremamente ineficiente e demorado. Além disso, salvar tudo em um único arquivo consolidado de 10 milhões de linhas a cada dia criaria arquivos gigantescos, difíceis de armazenar e processar. 

Para 10 milhões de linhas diárias, eu trocaria CSV por banco de dados, processamento em lote por processamento incremental e adicionaria monitoramento e checkpoints. Se o volume crescesse ainda mais, partiria para processamento distribuído com Spark

////////////////////////////////////////////////////////////////////////////////////////////////////

4 - Que testes você escreveria para garantir a qualidade das transformações?

Teste 1: Normalização de datas

Criar uma lista com datas nos formatos '2024-01-15', '15/01/2024' e '20240115'. Executar a função de normalização e verificar se todas se tornam o mesmo objeto datetime. Testar também valores vazios para garantir que retornam None. Se a data não converter corretamente, o cálculo de atraso vai falhar.

Teste 2: Normalização de valores monetários

Passar '150.50' e esperar 150.50. Passar '89,90' e esperar 89.90. Passar campo vazio e esperar 0.0. Se o valor não converter, o ticket médio por estado ficará incorreto.

Teste 3: Remoção de registros órfãos

Criar um pedido com id 101 e uma entrega com id_pedido 101, que deve ser mantida. Criar outra entrega com id_pedido 999, que não existe na tabela de pedidos, e verificar que ela é removida. Registros órfãos não têm informação útil e só prejudicam os indicadores.

Teste 4: Pipeline completo

Criar um conjunto pequeno e conhecido de dados de entrada com 3 pedidos. Executar o pipeline inteiro e comparar o arquivo consolidado gerado com um resultado esperado definido manualmente. Este teste garante que todas as etapas funcionam juntas.

Teste 5: Cálculo de atraso

Com data prevista 10/01 e data realizada 15/01, o atraso deve ser 5 dias. Com data prevista 10/01 e data realizada 05/01, o atraso deve ser -5 dias (antecipado). Com data realizada vazia, o atraso deve ser None. Este teste garante que a métrica de desempenho está correta.

Teste 6: Normalização de cidades

Passar 'São Paulo', 'sao paulo', 'SAO PAULO' e 'SP' e verificar que todos viram 'São Paulo'. Passar 'Rio de Janeiro' e 'rj' e verificar que viram 'Rio de Janeiro'. Se as cidades não forem padronizadas, o ranking de top 3 cidades ficará distorcido.



