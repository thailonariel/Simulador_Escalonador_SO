from fila import Fila

class SimulacaoEscalonador:
    def __init__(self, tempo_troca_coontexto):
        self.tempo_atual = 0
        self.tempo_troca_contexto = tempo_troca_coontexto
        self.fila_prontos = Fila()
        self.processos_finalizados = []
        self.ordem_execucao = []  # Para registrar a ordem de execução dos processos

    def executar_ciclo(self, processo):
        # Simula a CPU rodando por uma unidade de tempo
        if processo.tempo_inicio == -1:
            processo.tempo_inicio = self.tempo_atual

        processo.executar()
        self.ordem_execucao.append(processo.id)  # Registra o processo que está sendo execut
        self.tempo_atual += 1

        if processo.tempo_restante == 0:
            processo.tempo_fim = self.tempo_atual
            self.processos_finalizados.append(processo)
            return True  # Processo finalizado
        return False  # Processo ainda em execução  