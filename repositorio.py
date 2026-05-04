from processo import Processo

class RepositorioProcessos:
    def __init__(self):
        # Lista que armazena os objetos do tipo Processo
        self.processos = []

    def adicionar(self, p):
        # Adiciona um novo processo ao repositório
        self.processos.append(p)

    def listar(self):
        # Retorna a lista completa para o escalonador
        return self.processos