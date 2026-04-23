class Fila:
    def __init__(self):
        #O diagrama pede uma lista de processos
        self.processos = []

    def adicionar(self, p):
        #Requisito do UML
        self.processos.append(p)

    def remover(self):
        #Remove o próximo processo a ser executado
        if not self.estavazia():
            return self.processos.pop(0)
        return None
    
    def ordenar(self, criterio):
        # O UML pede um método de ordenar
        # Útil para o algoritmo SJF
        self.processos.sort(key=criterio)

    def estavazia(self):
        #Requisito do UML
        return len(self.processos) == 0

