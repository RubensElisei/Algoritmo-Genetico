import random

def calcular_fitness(cromossomo, pesos_e_valores, peso_maximo):
    peso_total = 0
    valor_total = 0
    for i in range(len(cromossomo)):
        if cromossomo[i] == 1:
            peso_total += pesos_e_valores[i][0]
            valor_total += pesos_e_valores[i][1]
    if peso_total > peso_maximo:
        return 0  # Penalidade por ultrapassar o peso máximo
    return valor_total

def gerar_populacao_inicial(tamanho_populacao, num_itens):
    return [[random.randint(0, 1) for _ in range(num_itens)] for _ in range(tamanho_populacao)]

def crossover(pai1, pai2):
    ponto_de_corte = random.randint(1, len(pai1) - 1)
    filho1 = pai1[:ponto_de_corte] + pai2[ponto_de_corte:]
    filho2 = pai2[:ponto_de_corte] + pai1[ponto_de_corte:]
    return filho1, filho2

def mutacao(cromossomo, taxa_mutacao):
    for i in range(len(cromossomo)):
        if random.random() < taxa_mutacao:
            cromossomo[i] = 1 - cromossomo[i]  # Inverte o bit
    return cromossomo

def selecao_torneio(populacao, fitness_populacao, tamanho_torneio=3):
    torneio = random.sample(range(len(populacao)), tamanho_torneio)
    melhor = max(torneio, key=lambda idx: fitness_populacao[idx])
    return populacao[melhor]

# Algoritmo genético
def algoritmo_genetico(pesos_e_valores, peso_maximo, num_cromossomos, geracoes, taxa_mutacao=0.1):  # Aumentar a taxa de mutação
    num_itens = len(pesos_e_valores)
    populacao = gerar_populacao_inicial(num_cromossomos, num_itens)
    
    melhor_individuo_por_geracao = []
    melhor_fitness_geral = 0
    melhor_individuo_geral = []
    
    for geracao in range(geracoes):
        fitness_populacao = [calcular_fitness(cromossomo, pesos_e_valores, peso_maximo) for cromossomo in populacao]
        
        nova_populacao = []
        
        while len(nova_populacao) < num_cromossomos:
            # Seleção
            pai1 = selecao_torneio(populacao, fitness_populacao)
            pai2 = selecao_torneio(populacao, fitness_populacao)
            
            # Garantir que os pais são diferentes
            while pai1 == pai2:
                pai2 = selecao_torneio(populacao, fitness_populacao)

            # Crossover
            filho1, filho2 = crossover(pai1, pai2)
            
            # Mutação
            filho1 = mutacao(filho1, taxa_mutacao)
            filho2 = mutacao(filho2, taxa_mutacao)
            
            nova_populacao.append(filho1)
            if len(nova_populacao) < num_cromossomos:  # Evitar adicionar filho2 se já tiver adicionado o suficiente
                nova_populacao.append(filho2)
        
        populacao = nova_populacao[:num_cromossomos]
        
        fitness_populacao = [calcular_fitness(cromossomo, pesos_e_valores, peso_maximo) for cromossomo in populacao]
        melhor_fitness = max(fitness_populacao)
        melhor_individuo = populacao[fitness_populacao.index(melhor_fitness)]
        melhor_individuo_por_geracao.append([melhor_fitness, melhor_individuo])
        
        # Verificar se esse é o melhor indivíduo de todas as gerações
        if melhor_fitness > melhor_fitness_geral:
            melhor_fitness_geral = melhor_fitness
            melhor_individuo_geral = melhor_individuo
    
    return melhor_fitness_geral, melhor_individuo_geral, melhor_individuo_por_geracao

# Parâmetros
pesos_e_valores = [[2, 10], [4, 30], [6, 300], [8, 10], [8, 30], [8, 300], [12, 50], [25, 75], [50, 100], [100, 400]]
peso_maximo = 100
num_cromossomos = 150
geracoes = 50

# Executar o algoritmo genético
melhor_fitness_geral, melhor_individuo_geral, melhor_individuo_por_geracao = algoritmo_genetico(pesos_e_valores, peso_maximo, num_cromossomos, geracoes)

# Exibir o resultado
print("Melhores individuos por geracao:")
for i, individuo in enumerate(melhor_individuo_por_geracao):
    print(f"Geracao {i+1}: Valor = {individuo[0]}, Cromossomo = {individuo[1]}")

# Exibir a melhor solução final
print(f"\nMelhor solucao final: Valor = {melhor_fitness_geral}, Cromossomo = {melhor_individuo_geral}")
