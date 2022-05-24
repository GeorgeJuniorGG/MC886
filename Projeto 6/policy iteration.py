from environment_simulator import mdp

def argmax(a0, a1, a2, a3):
    aux = max(max(a0, a1), max(a2, a3))
    if(aux == a0):
        return 0
    elif(aux == a1):
        return 1
    elif(aux == a2):
        return 2
    else:
        return 3

def policyIteration(states, actions, environment, utility, policy, gamma, reverseStates):
    naoMudou = False

    # Quando nao mudar, eh porque chegamos na politica otima, ja que estabilizou
    while(not naoMudou):

        naoMudou = True
        utility = policyEvaluation(policy, utility, gamma, environment)     # Calcula a utilidade para a politica em uso

        for i in range(9):

            if(policy[i] == 0):                                             # Decide a direcao para ir, de acordo com a politica
                direction = "left"
            elif(policy[i] == 1):
                direction = "right"
            elif(policy[i] == 3):
                direction = "down"
            else:
                direction = "up"

            # Calcula o valor da recompensa esperada utilizando a politica
            anterior = environment.getReward(states[i])
            for (newS, prob) in environment.getTransitionProbabilities(states[i], direction):
                anterior +=  gamma * prob * utility[reverseStates[newS]]

            # Determina se existe alguma acao que aumenta o valor da recompensa esperada
            a0 = environment.getReward(states[i])
            a1 = a0
            a2 = a0
            a3 = a0

            for (newS, prob) in environment.getTransitionProbabilities(states[i], "left"):
                a0 +=  gamma * prob * utility[reverseStates[newS]]
            
            for (newS, prob) in environment.getTransitionProbabilities(states[i], "right"):
                a1 +=  gamma * prob * utility[reverseStates[newS]]
            
            for (newS, prob) in environment.getTransitionProbabilities(states[i], "up"):
                a2 +=  gamma * prob * utility[reverseStates[newS]]

            for (newS, prob) in environment.getTransitionProbabilities(states[i], "down"):
                a3 +=  gamma * prob * utility[reverseStates[newS]]

            a = argmax(a0, a1, a2, a3)
            if(max(max(a0, a1), max(a2, a3)) > anterior):
                policy[i] = a
                naoMudou = False

    return policy

# Calcula pelo metodo do ponto fixo
def policyEvaluation(policy, utility, gamma, environment):
    n = 25                          # Numero de iteracoes que determinei empiricamente para a aproximacao
    for i in range (n):
        for j in range(9):
            if(policy[j] == 0):
                direction = "left"
            elif(policy[j] == 1):
                direction = "right"
            elif(policy[j] == 3):
                direction = "down"
            else:
                direction = "up"

            utilityAux = environment.getReward(states[j])
            for (newS, prob) in environment.getTransitionProbabilities(states[j], direction):
                utilityAux += gamma * prob * utility[reverseStates[newS]]
            utility[j] = utilityAux
    return utility

environment = mdp((1,1))

# Valor de gamma definido com base no que foi dito em sala
gamma = 1

# Mapeamento de identificadores de estados
# OBS: o estado (2,2) nao esta presente pois ele corresponde a uma parede
states =   {0: (1,1), 1: (1,2), 2: (1,3), 
            3: (2,1), 4: (2,3),
            5: (3,1), 6: (3,2), 7:(3,3),
            8: (4,1), 9: (4,2), 10: (4,3)}
reverseStates ={(1,1): 0, (1,2): 1, (1,3):2, 
                (2,1): 3, (2,3): 4,
                (3,1): 5, (3,2): 6, (3,3): 7,
                (4,1): 8, (4,2): 9, (4,3): 10}

# Vetor de acoes
# 0 corresponde a ir para a esquerda, 1 para a direita, 2 para cima e 3 para baixo
actions = [0, 1, 2, 3]

# Vetor inicial de política (quaisquer valores)
# Em cada posição, temos a politica para cada estado: 0 corresponde a ir para a esquerda, 1 para a direita, 2 para cima e 3 para baixo
# OBS: Nao existe politica para os estados terminais porque eles ja sao o final do problema
policy = [0, 1, 2,
          0, 1,
          0, 1, 2,
          0]

# Vetor inicial de utilidade (inicializados com 0)
# OBS: A utilidade eh o proprio valor de recompensa para os estados terminais porque eles ja sao o final do problema
utility = [0, 0, 0,
           0, 0,
           0, 0, 0,
           0, -1, 1]

# Obter a politica otima
optimalPolicy = policyIteration(states, actions, environment, utility, policy, gamma, reverseStates)

# Vetor inicial de valores esperados (inicializados com 0)
expectedValue = [0, 0, 0,
                 0, 0,
                 0, 0, 0,
                 0, -1, 1]

# Este loop calcula o valor esperado de cada estado, a partir de multiplas simulacoes
for i in range (9):             # Nao estou incluindo os estados terminais
    n = 10000                               # Numero de simulacoes
    accum = 0                               # Acumula as somas das recompensas de todas as simulacoes

    for j in range (n):                             # Faz as n simulacoes
        state = states[i]                           # Reseta o estado inicial para cada simulacao
        accum2 = environment.getReward(state)       # Reseta o acumulador interno para cada simulacao
        while state not in environment.terminalStates:
            aux = optimalPolicy[reverseStates[state]]   # Escolhe a direcao para ir com base na politica otima
            if(aux == 0):
                direction = "left"
            elif (aux == 1):
                direction = "right"
            elif (aux == 3):
                direction = "down"
            else:
                direction = "up"

            (state, reward) = environment.getDestination(state, direction)  # Pega o proximo estado e a recompensa atrelada a ele
            accum2 += reward

        accum += accum2                     # Atualiza o acumulador externo

    expectedValue[i] = accum/n              # Calcula a media de valores esperados

# Saida
print("Politica Otima: ")
for i in range(3,0,-1):
    for j in range(1,5):
        if (i, j) == (2,2):
            char = '#'
        elif (i,j) == (3,4) or (i,j) == (2,4):
            char = "T"
        else:
            aux = optimalPolicy[reverseStates[(j, i)]]
            if(aux == 0):
                char = "L"
            elif (aux == 1):
                char = "R"
            elif (aux == 3):
                char = "D"
            else:
                char = "U"
        print(char, end=" ")
    print("")
print("L = Left, R = Right, U = Up, D = Down, # = Hole, T = Terminal State")
print("#########################################################")
print("Valor Esperado de Cada Estado:")
for i in range(3,0,-1):
    for j in range(1,5):
        if (i, j) == (2,2):
            print("  #  ", end="")
        else:
            char = expectedValue[reverseStates[(j,i)]]
            print("%.2f" %char,end=" ")
    print("")
print("#########################################################")
print("Utilidade de Cada Estado:")
for i in range(3,0,-1):
    for j in range(1,5):
        if (i, j) == (2,2):
            print("  #  ", end="")
        else:
            char = utility[reverseStates[(j,i)]]
            print("%.2f" %char,end=" ")
    print("")