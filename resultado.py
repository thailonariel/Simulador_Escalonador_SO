class ResultadoSimulacao:
    def __init__(self):
        self.ordem_execucao = []
        self.tempos_execucao = {} # PID -> Tempo Efetivo
        self.tempos_espera = {}   # PID -> Tempo de Espera

    def registrar_execucao(self, pid):
        # Registra a sequência de PIDs (sem duplicar seguidos)
        if not self.ordem_execucao or self.ordem_execucao[-1] != pid:
            self.ordem_execucao.append(pid)

    def registrar_tempo(self, processo):
        # Tempo Efetivo (Turnaround): Fim - Chegada
        tempo_efetivo = processo.tempo_fim - processo.tempo_chegada
        self.tempos_execucao[processo.id] = tempo_efetivo
        
        # Tempo de Espera: Tempo Efetivo - Tempo de Execução Original
        tempo_espera = tempo_efetivo - processo.tempo_execucao
        self.tempos_espera[processo.id] = tempo_espera

    def calcular_media_espera(self):
        if not self.tempos_espera:
            return 0.0
        total_espera = sum(self.tempos_espera.values())
        return total_espera / len(self.tempos_espera)