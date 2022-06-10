from collections import defaultdict
from environment_simulator import mdp

# Calcula pelo metodo do ponto fixo
def policyEvaluation(policy, utility, gamma, rewards, Prob, states, reverseStates):
    n = 25                          # Numero de iteracoes que determinei empiricamente para a aproximacao
    for i in range (n):
        for j in range(11):
            if(policy[j] == 0):
                direction = "left"
            elif(policy[j] == 1):
                direction = "right"
            elif(policy[j] == 3):
                direction = "down"
            else:
                direction = "up"
            utilityAux = rewards[states[j]]

            for dic in Prob[states[j]][direction]:
                newS = dic
                prob = Prob[states[j]][direction][newS]
                utilityAux += gamma * prob * utility[reverseStates[newS]]

            utility[j] = utilityAux

    return utility

def directUtilityEstimation (policy, environment, states, reverseStates, limite):

    utilidade = [0, 0, 0,
                 0, 0,
                 0, 0, 0,
                 0, 0, 0]
    
    happened =  [1, 1, 1,    # Vetor que indica se ja foi encontrado algum valor de utilidade para os estados
                 1, 1,
                 1, 1, 1,
                 1, 1, 1]
    convergiu = [0, 0, 0,
                 0, 0,
                 0, 0, 0,
                 0, 0, 0]
    conv = False

    for i in range (200000):
        count = 0
        hist_estados = []        # Guarda os estados visitados
        hist_recompensas = []    # Guarda as recompensas recebidas

        utilidadeAux = [10, 10, 10, # Valores dummies para indicar que nao foi setado nenhum valor
                 10, 10,
                 10, 10, 10,
                 10, 10, 10]
        
        ocorrencias =  [0, 0, 0,
                        0, 0,
                        0, 0, 0,
                        0, 0, 0]         # Conta se algum estado foi alcancado mais de uma vez

        estado = (1,1)
        recompensa = -0.04

        hist_estados.append(estado)
        hist_recompensas.append(recompensa)
        ocorrencias[reverseStates[estado]] += 1

        while (estado not in environment.terminalStates):
            aux = policy[reverseStates[estado]]
            if(aux == 0):
                direction = "left"
            elif (aux == 1):
                direction = "right"
            elif (aux == 3):
                direction = "down"
            else:
                direction = "up"

            estado, recompensa = environment.getDestination(estado, direction)
            hist_estados.append(estado)
            hist_recompensas.append(recompensa)
            ocorrencias[reverseStates[estado]] += 1
            count += 1
            if count > 1000:
                return -1

        for j in range(len(hist_estados)):
            if(utilidadeAux[reverseStates[hist_estados[j]]] == 10):
                utilidadeAux[reverseStates[hist_estados[j]]] = sum(hist_recompensas[j:])
            else:
                utilidadeAux[reverseStates[hist_estados[j]]] += sum(hist_recompensas[j:])
        
        for j in range(11):
            if(utilidadeAux[j] == 10):
                utilidadeAux[j] = 0
            elif(ocorrencias[j] > 1):
                utilidadeAux[j] = utilidadeAux[j] / ocorrencias[j]
 
        for j in range(11):
            if(utilidadeAux[j] != 0):
                if(happened[j] == 0):
                    utilidade[j] = (utilidade[j] + utilidadeAux[j]) /2
                else:
                    utilidade[j] = utilidadeAux[j]
                    happened[j] = 0
        conv = True
        for j in range(len(utilidade)):
            if(abs(convergiu[j] - utilidade[j]) > limite):
                conv = False
            convergiu[j] = utilidade[j]
        if (conv == True and i>200):
            print("DUE convergiu em: " + str(i))
            break

    return utilidade

def TD (policy, environment, states, reverseStates, gamma, limite):
    utilidade = [0, 0, 0,
                 0, 0,
                 0, 0, 0,
                 0, 0, 0]

    N_estado = [0, 0, 0,
                 0, 0,
                 0, 0, 0,
                 0, 0, 0]
    convergiu = [0, 0, 0,
                 0, 0,
                 0, 0, 0,
                 0, 0, 0]
    conv = False

    # De acordo com o livro
    alfa = lambda n: 60./(59+n)

    for i in range(200000):
        count = 0
        estado = (1,1)
        recompensa = -0.04
        prevRecompensa = 10
        prevEstado = -1

        if(N_estado[reverseStates[estado]] == 0):
            utilidade[reverseStates[estado]] = recompensa
        
        if(prevEstado != -1):
            N_estado[reverseStates[prevEstado]] += 1
            utilidade[reverseStates[prevEstado]] += alfa(N_estado[reverseStates[prevEstado]]) * (prevRecompensa + gamma * utilidade[reverseStates[estado]] - utilidade[reverseStates[prevEstado]])

        prevEstado = estado
        prevRecompensa = recompensa

        while(estado not in environment.terminalStates):

            aux = policy[reverseStates[estado]]
            if(aux == 0):
                direction = "left"
            elif (aux == 1):
                direction = "right"
            elif (aux == 3):
                direction = "down"
            else:
                direction = "up"

            estado, recompensa = environment.getDestination(estado, direction)

            if(N_estado[reverseStates[estado]] == 0):
                utilidade[reverseStates[estado]] = recompensa
        
            if(prevEstado != -1):
                N_estado[reverseStates[prevEstado]] += 1
                utilidade[reverseStates[prevEstado]] += alfa(N_estado[reverseStates[prevEstado]]) * (prevRecompensa + gamma * utilidade[reverseStates[estado]] - utilidade[reverseStates[prevEstado]])

            if (estado not in environment.terminalStates):
                prevEstado = estado
                prevRecompensa = recompensa
                
            else:
                prevEstado = -1
                prevRecompensa = 10

            count += 1
            if count > 1000:
                return -1

        conv = True
        for j in range(len(utilidade)):
            if(abs(convergiu[j] - utilidade[j]) > limite):
                conv = False
            convergiu[j] = utilidade[j]
        if (conv == True and i>200):
            print("TD convergiu em: " + str(i))
            break

    return utilidade

def ADP (policy, environment, states, reverseStates, gamma, limite):
    utilidade = [0, 0, 0,
                 0, 0,
                 0, 0, 0,
                 0, 0, 0]
    
    convergiu = [0, 0, 0,
                 0, 0,
                 0, 0, 0,
                 0, 0, 0]
    conv = False

    visitados = set()
    N_prevEstado_prevDir = defaultdict(int)
    N_estado_prevEstado_prevDir = defaultdict(int)
    
    P = {(1,1):{"left": {}, 
                "right": {}, 
                "up": {}, 
                "down": {}}, 
         (1,2):{"left": {}, 
                "right": {}, 
                "up": {}, 
                "down": {}}, 
        (1,3): {"left": {}, 
                "right": {}, 
                "up": {}, 
                "down": {}},
        (2,1): {"left": {}, 
                "right": {}, 
                "up": {}, 
                "down": {}}, 
        (2,2): {"left": {}, 
                "right": {}, 
                "up": {}, 
                "down": {}}, 
        (2,3): {"left": {}, 
                "right": {}, 
                "up": {}, 
                "down": {}}, 
        (3,1): {"left": {}, 
                "right": {}, 
                "up": {}, 
                "down": {}}, 
        (3,2): {"left": {}, 
                "right": {}, 
                "up": {}, 
                "down": {}}, 
        (3,3): {"left": {}, 
                "right": {}, 
                "up": {}, 
                "down": {}},
        (4,1): {"left": {}, 
                "right": {}, 
                "up": {}, 
                "down": {}}, 
        (4,2): {"left": {}, 
                "right": {}, 
                "up": {}, 
                "down": {}}, 
        (4,3): {"left": {}, 
                "right": {}, 
                "up": {}, 
                "down": {}}}

    R = {(1,1): 0, (1,2): 0, (1,3): 0,
         (2,1): 0, (2,2): 0, (2,3): 0,
         (3,1): 0, (3,2): 0, (3,3): 0,
         (4,1): 0, (4,2): 0, (4,3): 0}
    
    for i in range(200000):
        count = 0
        estado = (1,1)
        prevEstado = -1
        recompensa = -0.04
        prevDirecao = -1

        if (estado not in visitados):
            visitados.add(estado)
            utilidade[reverseStates[estado]] = recompensa
            R[estado] = recompensa

        if(prevEstado != -1):
            N_prevEstado_prevDir[(prevEstado, prevDirecao)] += 1
            N_estado_prevEstado_prevDir[(estado, prevEstado, prevDirecao)] += 1
            # Para cada t tal que N estado|prevEstado prevDir [t, prevEstado, prevDir] seja diferente de 0
            for j in [estAtual for (estAtual, estAnt, dirAnt), ocorrencias in N_estado_prevEstado_prevDir.items() if ocorrencias != 0 and (estAnt, dirAnt) == (prevEstado, prevDirecao)]:
                P[prevEstado][prevDirecao][j] = N_estado_prevEstado_prevDir[(j, prevEstado, prevDirecao)] / N_prevEstado_prevDir[(prevEstado, prevDirecao)]

        
        utilidade = policyEvaluation(policy, utilidade, gamma, R, P, states, reverseStates)
        
        prevEstado = estado
        aux = policy[reverseStates[estado]]
        if(aux == 0):
            prevDirecao = "left"
        elif (aux == 1):
            prevDirecao = "right"
        elif (aux == 3):
            prevDirecao = "down"
        else:
            prevDirecao = "up"

        while(estado not in environment.terminalStates):

            aux = policy[reverseStates[estado]]
            if(aux == 0):
                direction = "left"
            elif (aux == 1):
                direction = "right"
            elif (aux == 3):
                direction = "down"
            else:
                direction = "up"

            estado, recompensa = environment.getDestination(estado, direction)

            if (estado not in visitados):
                visitados.add(estado)
                utilidade[reverseStates[estado]] = recompensa
                R[estado] = recompensa

            if(prevEstado != -1):
                N_prevEstado_prevDir[(prevEstado, prevDirecao)] += 1
                N_estado_prevEstado_prevDir[(estado, prevEstado, prevDirecao)] += 1
                # Para cada t tal que N estado|prevEstado prevDir [t, prevEstado, prevDir] seja diferente de 0
                for j in [estAtual for (estAtual, estAnt, dirAnt), ocorrencias in N_estado_prevEstado_prevDir.items() if ocorrencias != 0 and (estAnt, dirAnt) == (prevEstado, prevDirecao)]:
                    P[prevEstado][prevDirecao][j] = N_estado_prevEstado_prevDir[(j, prevEstado, prevDirecao)] / N_prevEstado_prevDir[(prevEstado, prevDirecao)]
   
            
            utilidade = policyEvaluation(policy, utilidade, gamma, R, P, states, reverseStates)
            if (estado not in environment.terminalStates):
                prevEstado = estado
                aux = policy[reverseStates[estado]]
                if(aux == 0):
                    prevDirecao = "left"
                elif (aux == 1):
                    prevDirecao = "right"
                elif (aux == 3):
                    prevDirecao = "down"
                else:
                    prevDirecao = "up"
            else:
                prevEstado = -1
                prevDirecao = -1
    
        conv = True
        for j in range(len(utilidade)):
            if(abs(convergiu[j] - utilidade[j]) > limite):
                conv = False
            convergiu[j] = utilidade[j]
        if (conv == True and i > 200):
            print("ADP convergiu em: " + str(i))
            break

    return utilidade

def printPolicy (policy, reverseStates):
    for i in range(3,0,-1):
        for j in range(1,5):
            if (i, j) == (2,2):
                char = '#'
            elif (i,j) == (3,4) or (i,j) == (2,4):
                char = "T"
            else:
                aux = policy[reverseStates[(j, i)]]
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

def printUtility (utility, reverseStates):
    for i in range(3,0,-1):
        for j in range(1,5):
            if (i, j) == (2,2):
                print("  #  ", end="")
            else:
                char = utility[reverseStates[(j,i)]]
                print("%.2f" %char,end=" ")
        print("")

environment = mdp((1,1))

# Valor de gamma definido com base no que foi feito no ultimo exercicio
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

# Vetor de política ótima (encontrado no exercicio anterior)
# Em cada posição, temos a politica para cada estado: 0 corresponde a ir para a esquerda, 1 para a direita, 2 para cima e 3 para baixo
# OBS: Nao existe politica para os estados terminais porque eles ja sao o final do problema
optimalPolicy = [2, 2, 1,
                 0,    1,
                 0, 2, 1,
                 0, 0, 0]

# Vetores de políticas aleatórias (apenas 2, como definido no enunciado)
randomPolicy1 = [1, 3, 3,
                 1,    0,
                 2, 2, 1,
                 0, 0, 0]
randomPolicy2 = [1, 2, 1,
                 1,    1,
                 2, 1, 3,
                 0, 0, 0] 

# Vetores de utilidade: um para cada algoritmo, para cada politica usada
utility1a = [0, 0, 0,
           0, 0,
           0, 0, 0,
           0, -1, 1]
utility1b = [0, 0, 0,
           0, 0,
           0, 0, 0,
           0, -1, 1]
utility1c = [0, 0, 0,
           0, 0,
           0, 0, 0,
           0, -1, 1]

utility2a = [0, 0, 0,
           0, 0,
           0, 0, 0,
           0, -1, 1]
utility2b = [0, 0, 0,
           0, 0,
           0, 0, 0,
           0, -1, 1]
utility2c = [0, 0, 0,
           0, 0,
           0, 0, 0,
           0, -1, 1]

utility3a = [0, 0, 0,
           0, 0,
           0, 0, 0,
           0, -1, 1]
utility3b = [0, 0, 0,
           0, 0,
           0, 0, 0,
           0, -1, 1]
utility3c = [0, 0, 0,
           0, 0,
           0, 0, 0,
           0, -1, 1]

# Chamadas dos metodos para as 3 politicas
limite = 0.0002
utility1a = directUtilityEstimation(optimalPolicy, environment, states, reverseStates, limite)
utility2a = TD(optimalPolicy, environment, states, reverseStates, gamma, limite)
utility3a = ADP(optimalPolicy, environment, states, reverseStates, gamma, limite)

utility1b = directUtilityEstimation(randomPolicy1, environment, states, reverseStates, limite)
utility2b = TD(randomPolicy1, environment, states, reverseStates, gamma, limite)
utility3b = ADP(randomPolicy1, environment, states, reverseStates, gamma, limite)

utility1c = directUtilityEstimation(randomPolicy2, environment, states, reverseStates, limite)
utility2c = TD(randomPolicy2, environment, states, reverseStates, gamma, limite)
utility3c = ADP(randomPolicy2, environment, states, reverseStates, gamma, limite)

# Saída
print("Política Ótima")
printPolicy(optimalPolicy, reverseStates)
print("")
print("Direct Utility Estimation")
printUtility(utility1a, reverseStates)
print("TD")
printUtility(utility2a, reverseStates)
print("ADP")
printUtility(utility3a, reverseStates)
print("=================================")
print("Política Aleatória 1")
printPolicy(randomPolicy1, reverseStates)
print("")
print("Direct Utility Estimation")
printUtility(utility1b, reverseStates)
print("TD")
printUtility(utility2b, reverseStates)
print("ADP")
printUtility(utility3b, reverseStates)
print("=================================")
print("Política Aleatória 2")
printPolicy(randomPolicy2, reverseStates)
print("")
print("Direct Utility Estimation")
printUtility(utility1c, reverseStates)
print("TD")
printUtility(utility2c, reverseStates)
print("ADP")
printUtility(utility3c, reverseStates)