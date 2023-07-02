
from abc import abstractmethod
from ga.genetic_algorithm import GeneticAlgorithm
from ga.problem import Problem
from ga.individual import Individual


class IntVectorIndividual(Individual):

    def __init__(self, problem: Problem, num_genes: int):
        super().__init__(problem, num_genes)

        # Vamos criar uma lista vazia, que vai ser o genoma
        self.genome = []

        # Vamos adicionar os inteiros de 1 a num_genes ao genoma
        for gene_index in range(1, num_genes + 1):
            self.genome.append(gene_index)

        # Vamos misturar os inteiros do genoma, usando o random da classe GeneticAlgorithm
        GeneticAlgorithm.rand.shuffle(self.genome)

    def swap_genes(self, other, index: int):
        aux = self.genome[index]
        self.genome[index] = other.genome[index]
        other.genome[index] = aux

    @abstractmethod
    def compute_fitness(self) -> float:
        pass

    @abstractmethod
    def better_than(self, other: "IntVectorIndividual") -> bool:
        pass
