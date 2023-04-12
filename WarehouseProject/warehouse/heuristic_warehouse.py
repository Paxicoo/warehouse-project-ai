from agentsearch.heuristic import Heuristic
from warehouse.warehouse_problemforSearch import WarehouseProblemSearch
from warehouse.warehouse_state import WarehouseState


class HeuristicWarehouse(Heuristic[WarehouseProblemSearch, WarehouseState]):

    def __init__(self):
        super().__init__()

    def compute(self, state: WarehouseState) -> float:
        goal_position = self.problem.goal_position
        manhattan_distance = abs(state.line_forklift - goal_position.line) + abs(state.column_forklift - goal_position.column)
        return manhattan_distance

    def __str__(self):
        return "Manhattan distance heuristic"

