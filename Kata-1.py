from datetime import datetime
from typing import List, Tuple

class Paciente:
    def __init__(self, nome: str, idade: int, urgencia: str, horario: str):
        self.nome = nome
        self.idade = idade
        self.urgencia_original = urgencia
        self.urgencia = self._calcular_urgencia_final(urgencia, idade)
        self.horario = datetime.strptime(horario, "%H:%M")

    def _calcular_urgencia_final(self, urgencia: str, idade: int) -> int:
        """
        Converte nível de urgência em número (quanto maior, mais prioritário)
        e aplica regras 4 e 5.
        """
        niveis = {
            "BAIXA": 1,
            "MÉDIA": 2,
            "ALTA": 3,
            "CRÍTICA": 4
        }
        
        prioridade = niveis[urgencia]
        
        # Regra 4: Idosos (60+) com urgência MÉDIA sobem para ALTA
        if idade >= 60 and urgencia == "MÉDIA":
            prioridade = niveis["ALTA"]
        
        # Regra 5: Menores de 18 ganham +1 nível
        if idade < 18:
            prioridade += 1
        
        # Limita no máximo ao nível CRÍTICA (4)
        return min(prioridade, 4)
    
    def __repr__(self):
        return f"{self.nome} ({self.idade}) - {self.urgencia_original} -> Prioridade {self.urgencia}"


def ordenar_fila(pacientes: List[Paciente]) -> List[Paciente]:
    """
    1. Maior prioridade (urgencia numérica)
    2. Dentro do mesmo nível, menor horário de chegada (FIFO)
    """
    return sorted(pacientes, key=lambda p: (-p.urgencia, p.horario))

if __name__ == "__main__":
    print("=" * 60)
    print("SISTEMA DE TRIAGEM - UNIMED")
    print("=" * 60)
    
    pacientes = []
    
    while True:
        print("\n" + "-" * 40)
        nome = input("Nome do paciente (ou 'sair' para encerrar): ")
        if nome.lower() == 'sair':
            break
        
        idade = int(input("Idade: "))
        
        print("Níveis: BAIXA | MÉDIA | ALTA | CRÍTICA")
        urgencia = input("Nível de urgência: ").upper()
        
        horario = input("Horário de chegada (HH:MM): ")
        
        pacientes.append(Paciente(nome, idade, urgencia, horario))
        print(f"✅ {nome} cadastrado com sucesso!")
    
    if pacientes:
        print("\n" + "=" * 60)
        print("FILA DE ATENDIMENTO ORDENADA")
        print("=" * 60)
        
        fila = ordenar_fila(pacientes)
        
        for i, p in enumerate(fila, 1):
            print(f"{i}º - {p.nome} | {p.idade} anos | {p.urgencia_original} | Prioridade: {p.urgencia} | Horário: {p.horario.strftime('%H:%M')}")
    else:
        print("Nenhum paciente cadastrado.")