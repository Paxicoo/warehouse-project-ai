from ga.genetic_algorithm import GeneticAlgorithm
from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation

class MutationSwap(Mutation):
    def __init__(self, probability):
        super().__init__(probability)

    def mutate(self, ind: IntVectorIndividual) -> None:
        num_genes = len(ind.genome)
        pos1 = GeneticAlgorithm.rand.randint(0, num_genes - 1)
        pos2 = pos1
        while pos1 == pos2:
            pos2 = GeneticAlgorithm.rand.randint(0, num_genes - 1)
        # Troca os genes de posição
        ind.genome[pos1], ind.genome[pos2] = ind.genome[pos2], ind.genome[pos1]

    def __str__(self):
        return "Swap Mutation (" + f'{self.probability}' + ")"
