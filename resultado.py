class ResultadoSimulacao:
    def __init__(self):
        self.ordem_execucao = []
        self.tempos_execucao = {}
        self.tempo_medio_espera = 0.0

    def registrar_execução(self, pid):
        if not self.ordem_execucao or self.ordem_execucao[-1] != pid:
            self.ordem_execucao.append(pid)

    def registrar_tempo(self, processo):
        # Tempo efetivo observado na simulação 
        tempo_efetivo = processo.tempo_fim - processo.tempo_chegada
        self.tempos_execucao[processo.id] = tempo_efetivo