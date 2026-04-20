import pandas as pd
import numpy as np
from datetime import datetime
import os



def criar_arquivos_exemplo():
    """Cria os 3 arquivos CSV com problemas intencionais"""
    
    
    clientes_data = {
        'id_cliente': [1, 2, 3, 4, 5],
        'nome': ['João Silva', 'Maria Santos', 'Carlos Souza', 'Ana Paula', 'Pedro Costa'],
        'cidade': ['São Paulo', 'sao paulo', 'SAO PAULO', 'Rio de Janeiro', 'Belo Horizonte'],
        'estado': ['SP', 'SP', 'SP', 'RJ', 'MG'],
        'data_cadastro': ['2020-01-15', '15/03/2019', '2021-06-20', '10/10/2020', '2022-01-01']
    }
    pd.DataFrame(clientes_data).to_csv('dados/clientes.csv', index=False)
    
    
    pedidos_data = {
        'id_pedido': [101, 102, 103, 104, 105, 106],
        'data_pedido': ['2024-01-10', '15/01/2024', '2024-02-20', '10/03/2024', '2024-03-25', '2024-04-01'],
        'id_cliente': [1, 2, 3, 4, 5, 1],
        'valor_total': ['150.50', '89,90', '230.00', '45,50', '320.75', ''],
        'status': ['CONCLUIDO', 'PENDENTE', 'CONCLUIDO', 'CANCELADO', 'CONCLUIDO', 'PENDENTE']
    }
    pd.DataFrame(pedidos_data).to_csv('dados/pedidos.csv', index=False)
    
    
    entregas_data = {
        'id_entrega': [1001, 1002, 1003, 1004, 1005],
        'id_pedido': [101, 102, 103, 104, 999],
        'data_prevista': ['2024-01-15', '20/01/2024', '2024-02-25', '15/03/2024', '2024-04-10'],
        'data_realizada': ['2024-01-14', '22/01/2024', '2024-02-28', '', ''],
        'status_entrega': ['ENTREGUE', 'ENTREGUE', 'ENTREGUE', 'ATRASADO', 'PENDENTE']
    }
    pd.DataFrame(entregas_data).to_csv('dados/entregas.csv', index=False)
    
    print(" Arquivos CSV de exemplo criados em 'dados/'")



def normalizar_data(valor):
    """Converte vários formatos de data para datetime"""
    if pd.isna(valor) or valor == '':
        return None
    
    valor_str = str(valor).strip()
    
    formatos = [
        '%Y-%m-%d',      # 2024-01-15
        '%d/%m/%Y',      # 15/01/2024
        '%Y%m%d',        # 20240115
    ]
    
    for formato in formatos:
        try:
            return datetime.strptime(valor_str, formato)
        except ValueError:
            continue
    
    
    try:
        return datetime.fromtimestamp(float(valor_str))
    except:
        pass
    
    return None

def normalizar_valor_monetario(valor):
    """Converte string com vírgula ou ponto para float"""
    if pd.isna(valor) or valor == '':
        return 0.0
    
    valor_str = str(valor).strip()
    
    
    if ',' in valor_str and '.' not in valor_str:
        valor_str = valor_str.replace(',', '.')
    
    
    valor_str = valor_str.replace('R$', '').strip()
    
    try:
        return float(valor_str)
    except ValueError:
        return 0.0

def normalizar_cidade(cidade):
    """Normaliza nomes de cidades (São Paulo, sao paulo, SAO PAULO → São Paulo)"""
    if pd.isna(cidade):
        return ''
    
    cidade_str = str(cidade).strip().lower()
    
    
    mapa = {
        'são paulo': 'São Paulo',
        'sao paulo': 'São Paulo',
        'sp': 'São Paulo',
        'rio de janeiro': 'Rio de Janeiro',
        'rj': 'Rio de Janeiro',
        'belo horizonte': 'Belo Horizonte',
        'bh': 'Belo Horizonte'
    }
    
    return mapa.get(cidade_str, cidade_str.title())

def calcular_atraso(data_realizada, data_prevista):
    """Calcula dias de atraso (negativo = antecipado)"""
    if data_realizada is None or data_prevista is None:
        return None
    return (data_realizada - data_prevista).days



def executar_pipeline():
    """Executa todo o pipeline de transformação"""
    
    print("\n" + "="*60)
    print(" PIPELINE DE TRANSFORMAÇÃO - KATA 4")
    print("="*60)
    
    
    os.makedirs('dados', exist_ok=True)
    
    
    criar_arquivos_exemplo()
    
    print("\n Lendo arquivos CSV...")
    
    
    pedidos = pd.read_csv('dados/pedidos.csv')
    clientes = pd.read_csv('dados/clientes.csv')
    entregas = pd.read_csv('dados/entregas.csv')
    
    print(f"   Pedidos: {len(pedidos)} registros")
    print(f"   Clientes: {len(clientes)} registros")
    print(f"   Entregas: {len(entregas)} registros")
    
   
    print("\n Aplicando limpeza dos dados...")
    
    
    pedidos['data_pedido'] = pedidos['data_pedido'].apply(normalizar_data)
    pedidos['valor_total'] = pedidos['valor_total'].apply(normalizar_valor_monetario)
    
    
    clientes['data_cadastro'] = clientes['data_cadastro'].apply(normalizar_data)
    clientes['cidade_normalizada'] = clientes['cidade'].apply(normalizar_cidade)
    
    
    entregas['data_prevista'] = entregas['data_prevista'].apply(normalizar_data)
    entregas['data_realizada'] = entregas['data_realizada'].apply(normalizar_data)
    
    
    entregas_validas = entregas[entregas['id_pedido'].isin(pedidos['id_pedido'])]
    entregas_removidas = len(entregas) - len(entregas_validas)
    if entregas_removidas > 0:
        print(f" Removidas {entregas_removidas} entregas com pedido inexistente (orphan records)")
    
    
    print("\n Consolidando dados...")
    
    
    consolidado = pedidos.merge(clientes, on='id_cliente', how='left')
    
    
    consolidado = consolidado.merge(entregas_validas, on='id_pedido', how='left')
    
    
    consolidado['atraso_dias'] = consolidado.apply(
        lambda row: calcular_atraso(row['data_realizada'], row['data_prevista']),
        axis=1
    )
    
  
    resultado = consolidado[[
        'id_pedido',
        'nome',
        'cidade_normalizada',
        'estado',
        'valor_total',
        'status',
        'data_pedido',
        'data_prevista',
        'data_realizada',
        'atraso_dias',
        'status_entrega'
    ]].copy()
    
    
    resultado.columns = [
        'id_pedido', 'nome_cliente', 'cidade_normalizada', 'estado',
        'valor_total', 'status_pedido', 'data_pedido',
        'data_prevista_entrega', 'data_realizada_entrega',
        'atraso_dias', 'status_entrega'
    ]
    
    
    resultado.to_csv('dados/consolidado.csv', index=False)
    print(f"Consolidado salvo em 'dados/consolidado.csv' ({len(resultado)} registros)")
    
    return resultado



def calcular_indicadores(df):
    """Calcula e exibe os indicadores de desempenho"""
    
    print("\n" + "="*60)
    print("INDICADORES DE DESEMPENHO")
    print("="*60)
    
    
    print("\n1️⃣ Total de pedidos por status:")
    status_counts = df['status_pedido'].value_counts()
    for status, qtd in status_counts.items():
        print(f"   {status}: {qtd} pedidos")
    
    
    print("\n2️⃣ Ticket médio por estado (R$):")
    ticket_medio = df.groupby('estado')['valor_total'].mean().round(2)
    for estado, valor in ticket_medio.items():
        print(f"   {estado}: R$ {valor:.2f}")
    
    
    print("\n3️⃣ Percentual de entregas:")
    entregas_validas = df[df['status_entrega'].notna()]
    
    if len(entregas_validas) > 0:
        no_prazo = len(entregas_validas[entregas_validas['atraso_dias'] <= 0])
        com_atraso = len(entregas_validas[entregas_validas['atraso_dias'] > 0])
        
        total = len(entregas_validas)
        print(f"   No prazo: {no_prazo} ({no_prazo/total*100:.1f}%)")
        print(f"   Com atraso: {com_atraso} ({com_atraso/total*100:.1f}%)")
    else:
        print("   Sem dados de entrega disponíveis")
    
    
    print("\n4️⃣ Top 3 cidades com maior volume de pedidos:")
    top_cidades = df['cidade_normalizada'].value_counts().head(3)
    for cidade, qtd in top_cidades.items():
        print(f"   {cidade}: {qtd} pedidos")
    
    
    print("\n5️⃣ Média de atraso:")
    pedidos_com_atraso = df[df['atraso_dias'] > 0]
    if len(pedidos_com_atraso) > 0:
        media_atraso = pedidos_com_atraso['atraso_dias'].mean()
        print(f"   Média de atraso: {media_atraso:.1f} dias")
    else:
        print("   Nenhum pedido com atraso registrado")
    
    print("\n" + "="*60)
    print("✅ Pipeline finalizado com sucesso!")
    print("="*60)


if __name__ == "__main__":
    
    df_consolidado = executar_pipeline()
    
    
    calcular_indicadores(df_consolidado)