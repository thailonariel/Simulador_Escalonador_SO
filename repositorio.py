from processo import Processo

class RepositorioProcessos:
    def __init__(self):
        # Lista que armazena os objetos do tipo Processo [cite: 39]
        self.processos = []

    def adicionar(self, p):
        # Adiciona um novo processo ao repositório [cite: 40]
        self.processos.append(p)

    def listar(self):
        # Retorna a lista completa para o escalonador [cite: 41, 42]
        return self.processos