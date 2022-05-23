import os

class mdp:

    def __init__(self, initialState) -> None:
        self.initialState = initialState
        self.terminalStates = ((4,2), (4,3))
        self.actions = {(1,1): {"left": (((1,1), 0.9), ((1,2), 0.1)), 
                                "right": (((2,1), 0.8), ((1,2), 0.1), ((1,1), 0.1)), 
                                "up": (((1,2), 0.8), ((2,1), 0.1), ((1,1), 0.1)), 
                                "down": (((1,1), 0.9), ((2,1), 0.1))}, 
                        (1,2): {"left": (((1,2), 0.8), ((1,1), 0.1), ((1,3), 0.1)), 
                                "right": (((1,2), 0.8), ((1,1), 0.1), ((1,3), 0.1)), 
                                "up": (((1,2), 0.2), ((1,3), 0.8)), 
                                "down": (((1,2), 0.2), ((1,1), 0.8))}, 
                        (1,3): {"left": (((1,3), 0.9), ((1,2), 0.1)), 
                                "right": (((1,3), 0.1), ((2,3), 0.8), ((1,2), 0.1)), 
                                "up": (((1,3), 0.9), ((2,3), 0.1)), 
                                "down": (((1,3), 0.1), ((2,3), 0.1), ((1,2), 0.8))},
                        (2,1): {"left": (((2,1), 0.2), ((1,1), 0.8)), 
                                "right": (((2,1), 0.2), ((3,1), 0.8)), 
                                "up": (((2,1), 0.8), ((1,1), 0.1), ((3,1), 0.1)), 
                                "down": (((2,1), 0.8), ((1,1), 0.1), ((3,1), 0.1))}, 
                        (2,2): {"left": 0, 
                                "right": 0, 
                                "up": 0, 
                                "down": 0}, 
                        (2,3): {"left": (((2,3), 0.2), ((1,3), 0.8)), 
                                "right": (((2,3), 0.2), ((3,3), 0.8)), 
                                "up": (((2,3), 0.8), ((1,3), 0.1), ((3,3), 0.1)), 
                                "down": (((2,3), 0.8), ((1,3), 0.1), ((3,3), 0.1))}, 
                        (3,1): {"left": (((3,1), 0.1), ((3,2), 0.1), ((2,1), 0.8)), 
                                "right": (((3,1), 0.1), ((3,2), 0.1), ((4,1), 0.8)), 
                                "up": (((3,2), 0.8), ((2,1), 0.1), ((4,1), 0.1)), 
                                "down": (((3,1), 0.8), ((2,1), 0.1), ((4,1), 0.1))}, 
                        (3,2): {"left": (((3,2), 0.8), ((3,1), 0.1), ((3,3), 0.1)), 
                                "right": (((4,2), 0.8), ((3,1), 0.1), ((3,3), 0.1)), 
                                "up": (((3,2), 0.1), ((4,2), 0.1), ((3,3), 0.8)), 
                                "down": (((3,2), 0.1), ((4,2), 0.1), ((3,1), 0.8))}, 
                        (3,3): {"left": (((2,3), 0.8), ((3,3), 0.1), ((3,2), 0.1)), 
                                "right": (((3,2), 0.1), ((4,3), 0.8), ((3,3), 0.1)), 
                                "up": (((2,3), 0.1), ((4,3), 0.1), ((3,3), 0.8)), 
                                "down": (((3,2), 0.8), ((2,3), 0.1), ((4,3), 0.1))},
                        (4,1): {"left": (((4,1), 0.1), ((3,1), 0.8), ((4,2), 0.1)), 
                                "right": (((4,1), 0.9), ((4,2), 0.1)), 
                                "up": (((4,2), 0.8), ((4,1), 0.1), ((3,2), 0.1)), 
                                "down": (((4,1), 0.9), ((3,1), 0.1))}, 
                        (4,2): {"left": 0, 
                                "right": 0, 
                                "up": 0, 
                                "down": 0}, 
                        (4,3): {"left": 0, 
                                "right": 0, 
                                "up": 0, 
                                "down": 0}}

        self.rewards = {(1,1): -0.04, (1,2): -0.04, (1,3): -0.04,
                        (2,1): -0.04, (2,2): -0.04, (2,3): -0.04,
                        (3,1): -0.04, (3,2): -0.04, (3,3): -0.04,
                        (4,1): -0.04, (4,2): -1   , (4,3): 1    }
    
    # Dadas uma posicao e uma direcao, simula qual sera o proximo estado do agente, retornando tambem a recompensa desse estado
    def getDestination(self, position, direction):
        rand = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)

        possibilities = []
        for i in self.actions[position][direction]:
            possibilities.append(i[1])

        previous = 0
        for i in range(len(possibilities)):
            if(previous + possibilities[i] >= rand):            # Determina qual sera o novo estado de acordo com o modelo de
                pos = i                                         # transicao estabelecido
                break
            previous += possibilities[i]

        newpos = self.actions[position][direction][pos][0]      # Corresponde ao novo estado do agente
        return (newpos, self.getReward(newpos))
    
    # Dada uma posicao, retorna a recompensa de chegar ate ela
    def getReward(self, position):
        return self.rewards[position]

    # Dadas uma posicao e uma direcao, retorna o modelo de transicao
    def getTransitionProbabilities(self, position, direction):
        return self.actions[position][direction]