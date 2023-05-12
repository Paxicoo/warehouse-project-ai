from ga.individual import Individual
from ga.genetic_operators.recombination import Recombination

class Recombination2(Recombination):

    def __init__(self, probability: float):
        super().__init__(probability)

    # Cycle Crossover (CX)

    # Este operador de recombinação preserva a ordem relativa dos genes.
    # Ele começa por identificar "ciclos" de genes que são trocados entre os dois pais.
    # Em seguida, os ciclos são alternadamente copiados de cada pai para criar a descendência.

    def recombine(self, ind1: Individual, ind2: Individual) -> None:
        size = len(ind1.genome)

        # Inicia os slices como -1
        offspring1 = [-1]*size
        offspring2 = [-1]*size

        # Preenche a primeira posição do primeiro slice com o primeiro gene do primeiro pai
        offspring1[0] = ind1.genome[0]

        # Pega o gene do segundo pai que está na primeira posição do primeiro pai
        gene = ind2.genome[0]

        # Continua até encontrar um ciclo
        while gene != ind1.genome[0]:
            index = ind1.genome.index(gene)
            offspring1[index] = ind1.genome[index]
            gene = ind2.genome[index]

        # Preenche as posições vazias do primeiro slice com os genes do segundo pai
        for ix in range(size):
            if offspring1[ix] == -1:
                offspring1[ix] = ind2.genome[ix]

        # O mesmo processo para o segundo slice
        offspring2[0] = ind2.genome[0]
        gene = ind1.genome[0]
        while gene != ind2.genome[0]:
            index = ind2.genome.index(gene)
            offspring2[index] = ind2.genome[index]
            gene = ind1.genome[index]
        for ix in range(size):
            if offspring2[ix] == -1:
                offspring2[ix] = ind1.genome[ix]

        ind1.genome = offspring1
        ind2.genome = offspring2

    def __str__(self):
        return "Cycle Crossover (" + f'{self.probability}' + ")"
