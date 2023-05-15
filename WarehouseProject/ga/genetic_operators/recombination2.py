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

        print("Individuo 1 Inicio CX:", ind1.genome)
        print("Individuo 2 Inicio CX:", ind2.genome)
        size = len(ind1.genome)

        # Inicia os slices como -1
        offspring1 = [-1]*size
        offspring2 = [-1]*size

        # Find cycles
        used_indices = []
        cycles = []
        for i in range(size):
            if i not in used_indices:
                cycle = [i]
                used_indices.append(i)
                next_index = ind1.genome.index(ind2.genome[i])
                while next_index != i:
                    cycle.append(next_index)
                    used_indices.append(next_index)
                    next_index = ind1.genome.index(ind2.genome[next_index])
                cycles.append(cycle)

        # Assign genes to offspring
        for i, cycle in enumerate(cycles):
            if i % 2 == 0:
                for index in cycle:
                    offspring1[index] = ind1.genome[index]
                    offspring2[index] = ind2.genome[index]
            else:
                for index in cycle:
                    offspring1[index] = ind2.genome[index]
                    offspring2[index] = ind1.genome[index]

        ind1.genome = offspring1
        ind2.genome = offspring2

        print("Individuo 1 Fim CX:", ind1.genome)
        print("Individuo 2 Fim CX:", ind2.genome)

    def __str__(self):
        return "Cycle Crossover (" + f'{self.probability}' + ")"
