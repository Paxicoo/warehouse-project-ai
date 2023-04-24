from ga.problem import Problem
from warehouse.warehouse_agent_search import WarehouseAgentSearch
from warehouse.warehouse_individual import WarehouseIndividual


class WarehouseProblemGA(Problem):
    def __init__(self, agent_search: WarehouseAgentSearch):
        # TODO
        self.forklifts = agent_search.forklifts
        self.products = agent_search.products
        self.agent_search = agent_search

    def generate_individual(self) -> "WarehouseIndividual":
        # TODO
        pass

        # fazer isto antes de criar um individuo
        # É IDÊNTICO AO KNAPSAK, VER EXERCICIO DA AULA

        # PARA vários indivíduos (ver chatGPT)
        # regras: sequencial, positivos, não se repete, apenas inteiros
        # como representar varios agentes no mesmo individuo... ?????

    def __str__(self):
        string = "# of forklifts: "
        string += f'{len(self.forklifts)}'
        string = "# of products: "
        string += f'{len(self.products)}'
        return string

