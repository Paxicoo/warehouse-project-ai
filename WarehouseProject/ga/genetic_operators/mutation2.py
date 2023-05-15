from ga.genetic_algorithm import GeneticAlgorithm
from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation

class Mutation2(Mutation):
    def __init__(self, probability):
        super().__init__(probability)

    # Swap Mutation

    # Este operador seleciona aleatoriamente dois genes no genoma e simplesmente troca as suas posições.
    # É uma abordagem simples, mas pode ser bastante eficaz para introduzir variação na população.

    def mutate(self, ind: IntVectorIndividual) -> None:

        print("Individuo Mutacao Inicio Swap:", ind.genome)
        num_genes = len(ind.genome)
        pos1 = GeneticAlgorithm.rand.randint(0, num_genes - 1)
        pos2 = pos1
        while pos1 == pos2:
            pos2 = GeneticAlgorithm.rand.randint(0, num_genes - 1)
        # Troca os genes de posição
        ind.genome[pos1], ind.genome[pos2] = ind.genome[pos2], ind.genome[pos1]

        print("Individuo Mutacao Fim Swap:", ind.genome)

    def __str__(self):
        return "Swap Mutation (" + f'{self.probability}' + ")"
