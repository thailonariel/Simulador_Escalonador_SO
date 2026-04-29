from processo import Processo
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
            if p.tempo_chegada <= escalonador.tempo_atual and p not in escalonador.fila_prontos.processos and p not in escalonador.processos_finalizados:
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
                resultado.registrar_execucao(p_atual.id)

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
                resultado.registrar_execucao(p_atual.id)

            resultado.registrar_tempo(p_atual)
        else:
            escalonador.tempo_atual += 1

    return resultado

def simular_sjf_p(repositorio, ttc):
    escalonador = SimulacaoEscalonador(ttc)
    resultado = ResultadoSimulacao()
    todos_processos = repositorio.listar()
    p_atual = None

    #Simulamos segundo a segundo
    while len(escalonador.processos_finalizados) < len(todos_processos):
        # 1. Verifica quem chegou agora
        for p in todos_processos:
            if p.tempo_chegada == escalonador.tempo_atual:
                escalonador.fila_prontos.adicionar(p)

        # 2. Ordena a fila pelo tempo restante (Shortest Remaining Time First)
        escalonador.fila_prontos.ordenar(lambda p: p.tempo_restante)

        if not escalonador.fila_prontos.estavazia():
            p_topo = escalonador.fila_prontos.processos[0] #Só espia o primeiro da fila

            # Lógica de preempção: Se o novo é menor que o que está rodando
            if p_atual is None or p_topo.tempo_restante < p_atual.tempo_restante:
                if p_atual is not None:
                    escalonador.fila_prontos.adicionar(p_atual) # Devolve atual para a fila
                    escalonador.trocar_contexto() # Troca de contexto por interrupção

                p_atual = escalonador.fila_prontos.remover()

            # 3. Executa apenas 1 ciclo
            terminou = escalonador.executar_ciclo(p_atual)
            resultado.registrar_execucao(p_atual.id)

            if terminou:
                resultado.registrar_tempo(p_atual)
                p_atual = None # Libera a CPU para o próximo segundo
        else:
            escalonador.tempo_atual += 1
    return resultado

def simular_round_robin(repositorio, ttc, quantum):
    escalonador = SimulacaoEscalonador(ttc)
    resultado = ResultadoSimulacao()
    todos_processos = repositorio.listar()

    #O round robin usa a fila estritamente por ordem de chegada
    while len(escalonador.processos_finalizados) < len(todos_processos):
        # 1. Adiciona quem chegou no tempo_atual
        for p in todos_processos:
            if p.tempo_chegada == escalonador.tempo_atual:
                escalonador.fila_prontos.adicionar(p)

        if not escalonador.fila_prontos.estavazia():
            p_atual = escalonador.fila_prontos.remover()

            # Troca de contexto se não for o primeiroprocesso
            if escalonador.tempo_atual > 0 and len(escalonador.ordem_execucao) > 0:
                escalonador.trocar_contexto()

            # Executa até terminarou até atingir o quantum
            tempo_no_quantum = 0
            while tempo_no_quantum < quantum and p_atual.tempo_restante > 0:
                terminou = escalonador.executar_ciclo(p.atual)
                resultado.registrar_execucao(p_atual.id)
                tempo_no_quantum += 1

                #No meio do quantum, novos processos podem chegar
                for p in todos_processos:
                    if p.tempo_chegada == escalonador.tempo_atual:
                        escalonador.fila_prontos.adicionar(p)

            if p_atual.tempo_restante > 0:
                #Não terminou, volta para o final da fila
                escalonador.fila_prontos.adicionar(p_atual)
            else:
                #Terminou, registra o tempo
                resultado.registrar_tempo(p_atual)
        else:
            escalonador.tempo_atual += 1

    return resultado

if __name__ == "__main__":
    # 1. Primeiro chamamos a função para cadastrar os dados
    repo = RepositorioProcessos()

    print("___ CADASTRO DE PROCESSOS ___ ")
    qtd = int(input("Quantos processos?    "))
    for i in range(qtd):
        pid = int(input(f"PID do processo {i+1}: "))
        chegada = int(input("Tempo de chegada: "))
        execucao = int(input("Tempo de execução: "))
        repo.adicionar(Processo(pid, chegada, execucao))

    # 2. Depois exibimos o menu de algoritmos
    print("\n--- ESCOLHA O ALGORITMO ---")
    print("1. FCFS")
    print("2. SJF (Não Preemptivo)")
    print("3. SJF (Preemptivo)")
    print("4. Round Robin")
    opcao = int(input("Opção: "))
    
    ttc = int(input("Tempo de Troca de Contexto (TTC): "))
    
    if opcao == 1:
        res = simular_fcfs(repo, ttc)
    elif opcao == 2:
        res = simular_sjf_np(repo, ttc)
    elif opcao == 3:
        res = simular_sjf_p(repo, ttc)
    elif opcao == 4:
        q = int(input("Valor do Quantum: "))
        res = simular_round_robin(repo, ttc, q)

    # 3. Exibimos os resultados
    print("\n--- RESULTADO FINAL ---")
    print(f"Ordem de Execução: {res.ordem_execucao}")
    
    for pid in res.tempos_execucao:
        print(f"PID {pid}: Tempo Efetivo = {res.tempos_execucao[pid]}s | Espera = {res.tempos_espera[pid]}s")
    
    print(f"\nTEMPO MÉDIO DE ESPERA: {res.calcular_media_espera():.2f}s")