import collections
import copy

from ga.individual_int_vector import IntVectorIndividual


class WarehouseIndividual(IntVectorIndividual):

    def __init__(self, problem: "WarehouseProblemGA", num_genes: int):
        super().__init__(problem, num_genes)
        self.max_distance = 0
        self.total_distance = 0
        self.number_of_collisions = 0

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
        self.max_distance = 0
        self.total_distance = 0
        agent_search = self.problem.agent_search
        # Número de produtos
        product_count = len(agent_search.products)
        # Último produto visitado
        last_product_cell = None
        # Índice do agente que está a pegar o produto
        agent_index = 0
        # A menos que o genoma comece com um agente, o primeiro agente é o primeiro a pegar um produto
        agent_cell = agent_search.forklifts[agent_index]
        # A saída é sempre a mesma
        exit_cell = agent_search.exit
        # Dicionário de distâncias entre células para cada agente
        distances = [0 for _ in range(len(agent_search.forklifts))]


        # TODO perguntar quais os pesos ideais e como saber se o fitness está bom

        # ir experimentando, ver se o numero de passos nao aumenta muito

        # TODO perguntar dicas de como penalizar o fitness quando há colisão de agentes
        # TODO perguntar dicas de como por os produtos a preto quando são apanhados
        # TODO perguntar extras para além dos que estão no enunciado
        # o numero de passos nao deve ser tao grande, dar prioridade
        pesoDistTotal = 0.5
        pesoDistMax = 0.5

        # Vamos percorrer o genoma
        for i, genome_value in enumerate(self.genome):
            # Verificar se o valor do genoma corresponde a um agente
            if genome_value > product_count:
                # Se houver um último produto visitado, calcular a distância do último produto à saída
                if last_product_cell is not None:
                    distance_last_product_to_exit = agent_search.distances.get(
                        ((last_product_cell.line, last_product_cell.column),
                         (exit_cell.line, exit_cell.column)), float('inf'))
                    distances[agent_index] += distance_last_product_to_exit
                    last_product_cell = None
                # Se não houver um último produto visitado, significa que o agente não vai pegar nenhum produto
                # então vamos calcular a distância do agente à saída
                else:
                    distance_agent_to_exit = agent_search.distances.get(
                        ((agent_cell.line, agent_cell.column),
                         (exit_cell.line, exit_cell.column)), float('inf'))
                    distances[agent_index] += distance_agent_to_exit

                # Vamos mudar para o agente correto com base no valor do genoma
                # genome_value - product_count é o index do agente na matriz de forklifts
                agent_index = genome_value - product_count
                agent_cell = agent_search.forklifts[agent_index]
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
                distances[agent_index] += distance
                # O último produto visitado passa a ser o produto atual
                last_product_cell = product_cell

        # Se houver um último produto visitado, calcular a distância do último produto à saída
        if last_product_cell is not None:
            distance_last_product_to_exit = agent_search.distances.get(
                ((last_product_cell.line, last_product_cell.column),
                 (exit_cell.line, exit_cell.column)), float('inf'))
            distances[agent_index] += distance_last_product_to_exit
        # Se não houver um último produto visitado, calcular a distância do agente à saída
        else:
            distance_agent_to_exit = agent_search.distances.get(
                ((agent_cell.line, agent_cell.column),
                 (exit_cell.line, exit_cell.column)), float('inf'))
            distances[agent_index] += distance_agent_to_exit

        # Calcular a distância total percorrida por todos os agentes
        self.total_distance = sum(distances)
        # Calcular a distância máxima percorrida por um agente
        self.max_distance = max(distances)
        # Calcular o fitness
        self.fitness = pesoDistTotal * self.total_distance + pesoDistMax * self.max_distance

        # Obtain paths for all agents
        #forklift_paths, max_steps= self.obtain_all_path()

        # Detect collisions and penalize fitness
        #collision_penalty = 0.1  # Define a penalty constant
        #number_of_collisions = self.detect_collisions(forklift_paths)  # Get the number of collisions
        #self.fitness += self.fitness*(collision_penalty * number_of_collisions)  # Penalize fitness for each collision

        return self.fitness

    def obtain_all_path(self):

        # celulas todas que cada agente tem de percorrer (é uma matriz de agentes com celulas)

        # ou seja, basicamente isto é so para a interface gráfica, para mostrar o caminho que cada agente faz

        # steps é o numero maximo de passos que o agente pode dar

        # forklift_path é a matriz de celulas que cada linha representa as celulas que cada agente corre
        # se houver so um agente é um array, mas para ser generico criamos a matriz de dimensao por numero de agentes

        # tens que obter as celulas todas que cada par

        # guardar em cada par as cells que cada um percorrey

        # adaptar a class solution (gui) devolver as celulas percorridas por uma solução
        # depois guardar em cada par essas celulas, depois aqui consoante a solução, temos o genoma
        # vamos buscar as celulas todas para concatenar e depois devolver o caminho total
        # tem que dar return do caminho total, para depois na gui desenhar o caminho todo

        agent_search = self.problem.agent_search
        product_count = len(agent_search.products)
        forklift_paths = []
        agent_cell = agent_search.forklifts[0]
        exit_cell = agent_search.exit
        last_product_cell = None
        # Vamos instanciar um array para guardar o caminho do agente atual
        path = []
        # Número maximo de passos que o agente pode dar
        max_steps = 0

        # Vamos percorrer o genoma
        for i, genome_value in enumerate(self.genome):

            # Verificar se o valor do genoma corresponde a um agente
            if genome_value > product_count:
                # Se houver um último produto visitado, ir buscar o caminho do último produto à saída
                if last_product_cell is not None:
                    path_last_product_to_exit = agent_search.paths.get(
                        ((last_product_cell.line, last_product_cell.column),
                         (exit_cell.line, exit_cell.column)), float('inf'))
                    path.extend(path_last_product_to_exit)
                    last_product_cell = None
                # Se não houver um último produto visitado, significa que o agente não vai pegar nenhum produto
                # então vamos buscar o caminho do agente à saída
                else:
                    path_agent_to_exit = agent_search.paths.get(
                        ((agent_cell.line, agent_cell.column),
                         (exit_cell.line, exit_cell.column)), float('inf'))
                    path.extend(path_agent_to_exit)

                # Vamos mudar para o agente correto com base no valor do genoma
                # genome_value - product_count é o index do agente na matriz de forklifts
                agent_cell = agent_search.forklifts[genome_value - product_count]
                # Vamos guardar o caminho do agente atual
                forklift_paths.append(path)
                if len(path) > max_steps:
                    max_steps = len(path)
                # Vamos instanciar um novo array para guardar o caminho do agente atual
                path = []
            # Se o valor do genoma corresponder a um produto
            else:
                # Buscar o caminho do agente (ou do último produto) ao produto atual
                product_cell = agent_search.products[genome_value - 1]
                # Se o agente ainda não pegou nenhum produto
                if last_product_cell is None:
                    # O agente vai para o primeiro produto
                    path_to_product = agent_search.paths.get(((agent_cell.line, agent_cell.column),
                                                           (product_cell.line, product_cell.column)), float('inf'))
                    path_to_product = copy.deepcopy(path_to_product)
                # Se o agente já pegou pelo menos um produto
                else:
                    # O agente vai do último produto ao produto atual
                    path_to_product = agent_search.paths.get(((last_product_cell.line, last_product_cell.column),
                                                           (product_cell.line, product_cell.column)), float('inf'))

                    # Se o caminho for infinita, significa que acedemos ao dicionário com a ordem errada da chave
                    if path_to_product == float('inf'):

                        path_to_product = agent_search.paths.get(((product_cell.line, product_cell.column),
                                                               (last_product_cell.line, last_product_cell.column)),
                                                              float('inf'))
                        # reverse the path_to_product
                        path_to_product = copy.deepcopy(path_to_product)
                        path_to_product.reverse()

                    if path_to_product != float('inf') and path_to_product:
                        del path_to_product[0]
                path.extend(path_to_product)

                # O último produto visitado passa a ser o produto atual
                last_product_cell = product_cell

        # Se houver um último produto visitado, ir buscar o caminho do último produto à saída
        if last_product_cell is not None:
            path_last_product_to_exit = agent_search.paths.get(
                ((last_product_cell.line, last_product_cell.column),
                 (exit_cell.line, exit_cell.column)), float('inf'))
            path_last_product_to_exit = copy.deepcopy(path_last_product_to_exit)
            if path_last_product_to_exit != float('inf') and path_last_product_to_exit:
                del path_last_product_to_exit[0]
            path.extend(path_last_product_to_exit)
            forklift_paths.append(path)
            if len(path) > max_steps:
                max_steps = len(path)
        # Se não houver um último produto visitado, calcular a distância do agente à saída
        else:
            path_agent_to_exit = agent_search.paths.get(
                ((agent_cell.line, agent_cell.column),
                 (exit_cell.line, exit_cell.column)), float('inf'))
            forklift_paths.append(path_agent_to_exit)
            if len(path) > max_steps:
                max_steps = len(path)

        return forklift_paths, max_steps

    # Função que deteta as colisões entre agentes
    def detect_collisions(self, forklift_paths):
        # Initialize a counter for collisions
        collisions = 0

        # Go through each time step
        max_steps = max(len(path) for path in forklift_paths)  # Maximum steps any forklift takes

        for step in range(max_steps):

            # Initialize an empty list to store the positions of forklifts at the current step
            positions = []

            # Now we go through each forklift's path
            for path in forklift_paths:

                # If the current step is within the length of the forklift's path, this means the forklift is still moving
                if step < len(path):
                    # We add the position of the forklift at the current step to the positions list
                    positions.append((path[step].line, path[step].column))

            # We use a Counter to count how many times each position occurs in the positions list
            position_counts = collections.Counter(positions)

            # We go through each value (count) in the position_counts dictionary
            for count in position_counts.values():

                # If a count is greater than 1, this means that more than one forklift is in the same position
                # This is a collision, so we increment the collisions counter
                if count > 1:
                    collisions += 1

        # Once we have checked all steps and all paths, we return the total number of collisions
        return collisions

    def __str__(self):
        string = 'Fitness: ' + f'{self.fitness}' + '\n'
        string += str(self.genome) + "\n\n"
        string += 'Max Distance:' + f'{self.max_distance}' + '\n'
        string += 'Total Distance:' + f'{self.total_distance}' + '\n'
        string += 'Number of Collisions:' + f'{self.number_of_collisions}' + '\n'
        return string

    def better_than(self, other: "WarehouseIndividual") -> bool:
        return True if self.fitness < other.fitness else False

    # __deepcopy__ is implemented here so that all individuals share the same problem instance
    def __deepcopy__(self, memo):
        new_instance = self.__class__(self.problem, self.num_genes)
        new_instance.genome = self.genome.copy()
        new_instance.fitness = self.fitness
        new_instance.max_distance = self.max_distance
        new_instance.total_distance = self.total_distance
        new_instance.number_of_collisions = self.number_of_collisions
        # TODO
        return new_instance
