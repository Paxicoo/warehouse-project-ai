
from abc import abstractmethod
from ga.problem import Problem
from ga.individual import Individual

class IntVectorIndividual(Individual):

    def __init__(self, problem: Problem, num_genes: int):
        super().__init__(problem, num_genes)
        # TODO

        # criar invidivuos com valores aleatores entre 1 e 20 (20 produtos)

        # depois disso, antes de tudo é criar os individuos
        # preencher o genoma na classe individual

        # individuos têm inteiros, os inteiros correspondem aos produtos
        # e a ordem do genoma é a ordem pela qual os produtos são apanhados
        # no final vai para a porta

        #o objetivo é criar um array de inteiros, com os números dos produtos não repetidos !!

        # na solução do algoritmo genético, vejo onde está o par (cell1 é o agent, cell2 é o inteiro do genoma)
        # por exemplo, no indivíduo: 1-2-3 calcula-se do agente ao produto 1, do produto 1 ao 2, do 2 ao 3, e do 3 à porta

        # o fitness desse indivíduo é a soma dos custos de cada par do genoma

        # depois é fazer o compute_fitness, é facil

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
