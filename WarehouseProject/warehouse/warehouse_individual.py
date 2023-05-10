from ga.individual_int_vector import IntVectorIndividual


class WarehouseIndividual(IntVectorIndividual):

    def __init__(self, problem: "WarehouseProblemGA", num_genes: int):
        super().__init__(problem, num_genes)
        # TODO

    def compute_fitness(self) -> float:
        # o fitness é a soma dos custos de cada par do genoma
        # o genoma é um array de inteiros, que representa a ordem pela qual o agente vai passar pelas celulas

        # na solução do algoritmo genético, vejo onde está o par (cell1 é o agent, cell2 é o inteiro do genoma)
        # por exemplo, no indivíduo: 1-2-3 calcula-se do agente ao produto 1, do produto 1 ao 2, do 2 ao 3, e do 3 à porta

        # depois, soma-se os custos de cada par
        # o fitness é a soma dos custos de cada par

        # fazer print do fitness para ver se está tudo bem
        # print(self.fitness)

        self.fitness = 0
        agent_search = self.problem.agent_search
        # Número de produtos
        product_count = len(agent_search.products)
        # Último produto visitado
        last_product_cell = None
        # A menos que o genoma comece com um agente, o primeiro agente é o primeiro a pegar um produto
        agent_cell = agent_search.forklifts[0]
        # A saída é sempre a mesma
        exit_cell = agent_search.exit

        # Vamos percorrer o genoma
        for i, genome_value in enumerate(self.genome):
            # Verificar se o valor do genoma corresponde a um agente
            if genome_value > product_count:
                # Se houver um último produto visitado, calcular a distância do último produto à saída
                if last_product_cell is not None:
                    distance_last_product_to_exit = agent_search.distances.get(
                        ((last_product_cell.line, last_product_cell.column),
                         (exit_cell.line, exit_cell.column)), float('inf'))
                    self.fitness += distance_last_product_to_exit
                    last_product_cell = None
                # Se não houver um último produto visitado, significa que o agente não vai pegar nenhum produto
                # então vamos calcular a distância do agente à saída
                else:
                    distance_agent_to_exit = agent_search.distances.get(
                        ((agent_cell.line, agent_cell.column),
                         (exit_cell.line, exit_cell.column)), float('inf'))
                    self.fitness += distance_agent_to_exit

                # Vamos mudar para o agente correto com base no valor do genoma
                # genome_value - product_count é o index do agente na matriz de forklifts
                agent_cell = agent_search.forklifts[genome_value - product_count]
            # Se o valor do genoma corresponder a um produto
            else:
                # Calcular a distância do agente (ou do último produto) ao produto atual
                product_cell = agent_search.products[genome_value - 1]
                # Se o agente ainda não pegou nenhum produto
                if last_product_cell is None:
                    # O agente vai para o primeiro produto
                    distance = agent_search.distances.get(((agent_cell.line, agent_cell.column),
                                                           (product_cell.line, product_cell.column)), float('inf'))
                # Se o agente já pegou pelo menos um produto
                else:
                    # O agente vai do último produto ao produto atual
                    distance = agent_search.distances.get(((last_product_cell.line, last_product_cell.column),
                                                           (product_cell.line, product_cell.column)), float('inf'))

                    # Se a distância for infinita, significa que acedemos ao dicionário com a ordem errada da chave
                    if distance == float('inf'):
                        distance = agent_search.distances.get(((product_cell.line, product_cell.column),
                                                               (last_product_cell.line, last_product_cell.column)),
                                                              float('inf'))

                self.fitness += distance
                # O último produto visitado passa a ser o produto atual
                last_product_cell = product_cell

        # Se houver um último produto visitado, calcular a distância do último produto à saída
        if last_product_cell is not None:
            distance_last_product_to_exit = agent_search.distances.get(
                ((last_product_cell.line, last_product_cell.column),
                 (exit_cell.line, exit_cell.column)), float('inf'))
            self.fitness += distance_last_product_to_exit
        # Se não houver um último produto visitado, calcular a distância do agente à saída
        else:
            distance_agent_to_exit = agent_search.distances.get(
                ((agent_cell.line, agent_cell.column),
                 (exit_cell.line, exit_cell.column)), float('inf'))
            self.fitness += distance_agent_to_exit

        return self.fitness

    def obtain_all_path(self):
        # TODO

        # celulas todas que cada agente tem de percorrer (é uma matriz de agentes com celulas)

        # ou seja, basicamente isto é so para a interface gráfica, para mostrar o caminho que cada agente faz

        # steps é o numero maximo de passos que o agente pode dar

        # forklift_path é a matriz de celulas que cada linha representa as celulas que cada agente corre
        # se houver so um agente é um array, mas para ser generico criamos a matriz de dimensao por numero de agentes

        # tens que obter as celulas todas que cada par

        # guardar em cada par as cells que cada um percorrey

        # adaptar a class solution (gui) devolver as celulas percorridas por uma solução
        # depois guardar em cada par essas celulas, depois aqui consoante a solução, temos o genoma
        # vamos buscar as celulas todas para concatenar e depois devolver o caminho todo
        # tem que dar return do caminho todo, para depois na gui desenhar o caminho todo

        pass

    def __str__(self):
        string = 'Fitness: ' + f'{self.fitness}' + '\n'
        string += str(self.genome) + "\n\n"
        # TODO
        return string

    def better_than(self, other: "WarehouseIndividual") -> bool:
        return True if self.fitness < other.fitness else False

    # __deepcopy__ is implemented here so that all individuals share the same problem instance
    def __deepcopy__(self, memo):
        new_instance = self.__class__(self.problem, self.num_genes)
        new_instance.genome = self.genome.copy()
        new_instance.fitness = self.fitness
        # TODO
        return new_instance
