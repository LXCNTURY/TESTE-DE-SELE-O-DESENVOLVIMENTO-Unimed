from datetime import datetime

class Paciente:
    def __init__(self, nome: str, idade: int, urgencia: str, horario: str):
        self.nome = nome
        self.idade = idade
        self.urgencia_original = urgencia
        self.horario = datetime.strptime(horario, "%H:%M")
        self.prioridade = self._calcular_prioridade()

    def _calcular_prioridade(self):
        niveis = {"BAIXA": 1, "MÉDIA": 2, "ALTA": 3, "CRÍTICA": 4}
        prioridade = niveis[self.urgencia_original]

        # Regra 4: Idoso (60+) com MÉDIA vira ALTA
        if self.idade >= 60 and self.urgencia_original == "MÉDIA":
            prioridade = 3

        # Regra 5: Menor de 18 ganha +1 nível
        if self.idade < 18:
            prioridade += 1

        return min(prioridade, 4)  # Limita no máximo 4 (CRÍTICA)


def ordenar_fila(pacientes):
    return sorted(pacientes, key=lambda p: (-p.prioridade, p.horario))


# ==================== TESTES UNITÁRIOS ====================

def test_regra_4():
    p = Paciente("Seu José", 65, "MÉDIA", "10:00")
    assert p.prioridade == 3, f"Esperado 3 (ALTA), mas foi {p.prioridade}"
    print("Regra 4: Idoso com MÉDIA vira ALTA")

def test_regra_4_borda():
    p = Paciente("Dona Maria", 60, "MÉDIA", "10:00")
    assert p.prioridade == 3, f"Esperado 3, mas foi {p.prioridade}"
    print("Regra 4 (borda): 60 anos exatos vira ALTA")

def test_regra_5():
    p = Paciente("Joãozinho", 15, "BAIXA", "10:00")
    assert p.prioridade == 2, f"Esperado 2 (MÉDIA), mas foi {p.prioridade}"
    print("Regra 5: Menor com BAIXA vira MÉDIA")

def test_regra_5_borda():
    p = Paciente("André", 18, "BAIXA", "10:00")
    assert p.prioridade == 1, f"Esperado 1 (BAIXA), mas foi {p.prioridade}"
    print("Regra 5 (borda): 18 anos NÃO ganha nível")

def test_ordenacao():
    pacientes = [
        Paciente("João", 30, "BAIXA", "09:00"),
        Paciente("Maria", 25, "CRÍTICA", "09:30"),
        Paciente("Pedro", 40, "ALTA", "09:15"),
    ]
    fila = ordenar_fila(pacientes)
    assert fila[0].nome == "Maria"
    assert fila[1].nome == "Pedro"
    assert fila[2].nome == "João"
    print("Ordenação: Prioridade respeitada")


# ==================== EXIBIR TABELA ====================

def exibir_tabela(pacientes):
    """Exibe os pacientes em formato de tabela"""
    print("\n" + "="*60)
    print(f"{'FILA DE ATENDIMENTO':^60}")
    print("="*60)
    print(f"{'Posição':<8} {'Nome':<20} {'Horário':<10} {'Prioridade':<10}")
    print("-"*60)
    
    for i, p in enumerate(pacientes, 1):
        # Mapeia prioridade para texto
        prioridade_texto = {1: "BAIXA", 2: "MÉDIA", 3: "ALTA", 4: "CRÍTICA"}[p.prioridade]
        print(f"{i:<8} {p.nome:<20} {p.horario.strftime('%H:%M'):<10} {prioridade_texto:<10}")
    
    print("="*60)


# ==================== EXECUTAR ====================

if __name__ == "__main__":
    print("\n=== TESTES DO SISTEMA DE TRIAGEM ===\n")
    
    test_regra_4()
    test_regra_4_borda()
    test_regra_5()
    test_regra_5_borda()
    test_ordenacao()
    
    print("\nTodos os testes passaram!\n")
    
    # ========== EXEMPLO PRÁTICO COM TABELA ==========
    
    # Lista de pacientes
    pacientes = [
        Paciente("João Silva", 30, "BAIXA", "09:00"),
        Paciente("Maria Santos", 65, "MÉDIA", "09:05"),    # Regra 4: idoso + média
        Paciente("Pedro Costa", 15, "BAIXA", "09:10"),     # Regra 5: menor + baixa
        Paciente("Ana Paula", 25, "CRÍTICA", "09:15"),
        Paciente("Lucas Lima", 10, "MÉDIA", "09:20"),      # Regra 5: menor + média
        Paciente("José Ferreira", 70, "ALTA", "09:25"),
        Paciente("Carlos Alberto", 58, "MÉDIA", "09:30"),
    ]
    
    # Ordena a fila
    fila_ordenada = ordenar_fila(pacientes)
    
    # Exibe tabela
    exibir_tabela(fila_ordenada)