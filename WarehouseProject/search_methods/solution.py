from agentsearch.problem import Problem
from search_methods.node import Node
from warehouse.cell import Cell


class Solution:

    def __init__(self, problem: Problem, goal_node: Node):
        self.problem = problem
        self.goal_node = goal_node
        self.actions = []
        self.cells = []   # Stores the cells that the agent visited
        node = self.goal_node
        while node.parent is not None:
            self.actions.insert(0, node.state.action)
            self.cells.insert(0, Cell(node.state.line_forklift, node.state.column_forklift))
            node = node.parent
        self.cells.insert(0, Cell(node.state.line_forklift, node.state.column_forklift)) # adicionar o pai

    @property
    def cost(self) -> int:
        return self.problem.compute_path_cost(self.actions)

    def obtain_all_path(self):
        return self.cells
