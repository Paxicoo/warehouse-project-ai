from ga.genetic_algorithm import GeneticAlgorithm
from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation

class Mutation3(Mutation):
    def __init__(self, probability):
        super().__init__(probability)

    # Inversion Mutation

    # Este operador de mutação seleciona um subconjunto aleatório do genoma e inverte a ordem dos genes nesse subconjunto.
    # Pode fornecer diversidade à população sem alterar a ordem relativa dos genes dentro do subconjunto.

    def mutate(self, ind: IntVectorIndividual) -> None:
        num_genes = len(ind.genome)
        pos1 = GeneticAlgorithm.rand.randint(0, num_genes - 1)
        pos2 = pos1
        while pos1 == pos2:
            pos2 = GeneticAlgorithm.rand.randint(0, num_genes - 1)
        if pos1 > pos2:
            pos1, pos2 = pos2, pos1
        # Inverte a ordem dos genes no subconjunto selecionado
        ind.genome[pos1:pos2+1] = reversed(ind.genome[pos1:pos2+1])

    def __str__(self):
        return "Inversion Mutation (" + f'{self.probability}' + ")"
