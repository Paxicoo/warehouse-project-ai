from ga.genetic_algorithm import GeneticAlgorithm
from ga.genetic_operators.recombination import Recombination
from ga.individual import Individual

class Recombination3(Recombination):

    def __init__(self, probability: float):
        super().__init__(probability)

    # Order Crossover (OX)

    # Este operador de recombinação preserva a ordem relativa dos genes.
    # Ele começa por selecionar um segmento de genes de um dos pais.
    # Em seguida, ele preenche o restante do genoma com os genes do outro pai que ainda não estão presentes,
    # mantendo a sua ordem original.

    def recombine(self, ind1: Individual, ind2: Individual) -> None:
        print("Individuo 1 Inicio OX:", ind1.genome)
        print("Individuo 2 Inicio OX:", ind2.genome)
        size = len(ind1.genome)
        # Escolhe dois pontos aleatórios para o slice.
        start, end = sorted([GeneticAlgorithm.rand.randint(0, size - 1) for _ in range(2)])

        # Mantém o slice do primeiro pai, preenche o resto com os genes do segundo pai
        offspring1 = [-1] * size
        offspring1[start:end] = ind1.genome[start:end]
        gene_pointer = end
        for ix in range(size):
            if ind2.genome[(ix + end) % size] not in offspring1:
                offspring1[gene_pointer] = ind2.genome[(ix + end) % size]
                gene_pointer = (gene_pointer + 1) % size

        # Faz o mesmo para o segundo filho, mas em ordem inversa.
        offspring2 = [-1] * size
        offspring2[start:end] = ind2.genome[start:end]
        gene_pointer = end
        for ix in range(size):
            if ind1.genome[(ix + end) % size] not in offspring2:
                offspring2[gene_pointer] = ind1.genome[(ix + end) % size]
                gene_pointer = (gene_pointer + 1) % size

        ind1.genome = offspring1
        ind2.genome = offspring2

        print("Individuo 1 Fim OX:", ind1.genome)
        print("Individuo 2 Fim OX:", ind2.genome)
    def __str__(self):
        return "Order Crossover (" + f'{self.probability}' + ")"