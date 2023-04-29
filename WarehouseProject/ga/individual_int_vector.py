
from abc import abstractmethod
from ga.genetic_algorithm import GeneticAlgorithm
from ga.problem import Problem
from ga.individual import Individual


class IntVectorIndividual(Individual):

    def __init__(self, problem: Problem, num_genes: int):
        super().__init__(problem, num_genes)

        # criar invidivuos com valores aleatores entre 1 e 20 (se forem 20 produtos e apenas 1 agente)

        # depois disso, antes de tudo é criar os individuos
        # preencher o genoma na classe individual

        # individuos têm inteiros, os inteiros correspondem aos produtos
        # e a ordem do genoma é a ordem pela qual os produtos são apanhados
        # no final vai para a porta

        #o objetivo é criar um array de inteiros, com os números dos produtos não repetidos !!


        # o fitness desse indivíduo é a soma dos custos de cada par do genoma

        # depois é fazer o compute_fitness, é facil

        # no construtor, criar o genome, com valores entre 1 o tamanho
        # é aqui que vamos por o random (GeneticAlgorithm.rand.randint), preencher o genoma com valores aleatórios

        # NÃO ESQUECER QUE O TAMANHO DEPENDE SE EXISTE MAIS QUE UM AGENTE

        # no final fazer print(self.genome) para ver se está tudo bem


        # PARA vários indivíduos, é preciso criar um array de inteiros
        # regras: sequencial, positivos, não se repete, apenas inteiros
        # como representar varios agentes no mesmo individuo... ?????

        # agente 1, representado por "11" (produtos + 1), vai do produto 1 ao 4, agente 2, representado por "12" (produtos + 2)
        # vai do 5 ao 8, agente 3, representado por nenhum numero (não é necessário criar um inteiro no vetor para representar o ultimo agente
        # pois os ultimos produtos no array são os produtos que o ultimo agente vai apanhar), vai do 9 ao 10
        # [1, 2, 3, 4, 11, 5, 6, 7, 8, 12, 9, 10] --> 10 produtos, 3 agentes
        # [1, 2, 3, 4, 5, 6, 9, 7, 8] --> 8 produtos, 2 agentes (agente 1 vai do produto 1 ao 4, agente 2 vai do 5 ao 8)
        # 7 produtos e 1 agente --> [1, 2, 3, 4, 5, 6, 7], (agente 1 vai do produto 1 ao 7)
        # 6 produtos e 3 agentes --> [1, 7, 2, 3, 4, 8, 5, 6], (agente 1 vai do produto 1 ao 7, agente 2 vai do produto 2 ao 4, agente 3 vai do produto 5 ao 6)

        # É IMPORTANTE PARA O RANDOM (criar individuos aleatorios) QUE OS PRODUTOS NÃO SE REPITAM, USANDO A FUNÇÃO GeneticAlgorithm.rand.randint


        # Vamos criar uma lista vazia, que vai ser o genoma
        self.genome = []

        # Vamos adicionar os inteiros de 1 a num_genes ao genoma
        for gene_index in range(1, num_genes + 1):
            self.genome.append(gene_index)

        # Vamos misturar os inteiros do genoma, usando o random da classe GeneticAlgorithm
        GeneticAlgorithm.rand.shuffle(self.genome)

        # Print para debugging
        print(self.genome)

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
