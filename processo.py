class Processo:
    def __init__(self, pid, tempo_chegada, tempo_execucao):
        #Atributos exigidos pelo diagrama UML
        self.id = pid
        self.tempo_chegada = tempo_chegada
        self.tempo_execucao = tempo_execucao
        #Controle de tempo para algoritmos preemptivos
        self.tempo_restante = tempo_execucao
        self.tempo_inicio = -1
        self.tempo_fim = -1

    def executar(self):
        #Simula a execução de 1 unidade de tempo
        if self.tempo_restante > 0:
            self.tempo_restante -= 1

    def resetar(self):
        #Reseta o processo para permitir nova simulação
        self.tempo_restante = self.tempo_execucao
        self.tempo_inicio = -1
        self.tempo_fim = -1