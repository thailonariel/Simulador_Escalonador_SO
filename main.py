from repositorio import RepositorioProcessos
from escalonador import SimulacaoEscalonador
from resultado import ResultadoSimulacao

def simular_fcfs(repositorio, ttc):
    # Inicializamos o escalonador e o objeto de resultados
    escalonador = SimulacaoEscalonador(ttc)
    resultado = ResultadoSimulacao()

    #Pegamos todos os processos e ordenamos por tempo de chegada
    todos_processos = sorted(repositorio.listar(), key=lambda p: p.tempo_chegada)

    # O loop roda os processos enquanto houver processos para terminar
    while len(escalonador.processos_finalizados) < len(todos_processos):

        #1, Adiciona quem chegou na fila de prontos
        for p in todos_processos:
            if p.tempo_chegada == escalonador.tempo_atual:
                escalonador.fila_prontos.adicionar(p)

        #2. Se a fila não estiver vazia, pegamos o próximos (FCFS)
        if not escalonador.fila_prontos.estavazia():
            p_atual = escalonador.fila_prontos.remover()

            # Se não é o primeiro processo da simulação, ocorre a Troca de Contexto
            if escalonador.tempo_atual > 0 and len(escalonador.ordem_execucao) > 0:
                escalonador.trocar_contexto()

            #3. Executa o processo até terminar
            while p_atual.tempo_restante > 0:
                terminou = escalonador.executar_ciclo(p_atual)
                resultado.registrar_execução(p_atual.id)

            #Ao terminar, registra os tempos finais
            resultado.registrar_tempo(p_atual)

        else:
            # Se ninguem chegou ainda, o tempo passa
            escalonador.tempo_atual += 1

    return resultado

def simular_sjf_np(repositorio, ttc):
    escalonador = SimulacaoEscalonador(ttc)
    resultado = ResultadoSimulacao()
    todos_processos = repositorio.listar()

    while len(escalonador.processos_finalizados) < len(todos_processos):
        # 1. Adiciona quem chegou no tempo atual
        for p in todos_processos:
            if p.tempo_chegada == escalonador.tempo_atual:
                escalonador.fila_prontos.adicionar(p)

        if not escalonador.fila_prontos.estavazia():
            # Antes de remover, ordenamos pelo menor tempo de execução
            escalonador.fila_prontos.ordenar(lambda p: p.tempo_execucao)

            p_atual = escalonador.fila_prontos.remover()

            if escalonador.tempo_atual > 0 and len(escalonador.ordem_execucao) > 0:
                escalonador.trocar_contexto()

            while p_atual.tempo_atual > 0:
                escalonador.executar_ciclo(p_atual)
                resultado.registrar_execução(p_atual.id)

            resultado.registrar_tempo(p_atual)
        else:
            escalonador.tempo_atual += 1

    return resultado