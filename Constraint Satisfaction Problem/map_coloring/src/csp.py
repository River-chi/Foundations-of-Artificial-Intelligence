from collections import deque
from copy import deepcopy

# AC-3
def ac3(domains: dict, neighbours: dict) -> bool:
    # Initialise the work queue with every directed arc (Xi, Xj)
    queue = deque()
    for xi in domains:
        for xj in neighbours[xi]:
            queue.append((xi, xj))

    removed_count = 0

    while queue:
        xi, xj = queue.popleft()
        if _revise(domains, xi, xj):
            removed_count += 1
            if len(domains[xi]) == 0:
                return False
            for xk in neighbours[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True

def _revise(domains: dict, xi: str, xj: str) -> bool:
    revised = False
    for x in list(domains[xi]):
        if not any(x != y for y in domains[xj]):
            domains[xi].remove(x)
            revised = True
    return revised

# Backtracking search
def backtracking_search(variables: list,
                        domains_orig: dict,
                        neighbours: dict) -> dict | None:
    # Run AC-3 once before search to reduce domains
    domains = deepcopy(domains_orig)
    if not ac3(domains, neighbours):
        return None

    return _backtrack({}, variables, domains, neighbours)

def _backtrack(assignment: dict, variables: list,
               domains: dict, neighbours: dict) -> dict | None:
    if len(assignment) == len(variables):
        return assignment

    var = _select_unassigned_var(assignment, variables, domains)
    for value in _order_domain_values(var, assignment, domains, neighbours):
        if _is_consistent(var, value, assignment, neighbours):
            assignment[var] = value
            new_domains = deepcopy(domains)
            new_domains[var] = {value}
            if ac3(new_domains, neighbours):
                result = _backtrack(assignment, variables,
                                    new_domains, neighbours)
                if result is not None:
                    return result
            del assignment[var]

    return None

# Heuristics
def _select_unassigned_var(assignment: dict, variables: list,
                            domains: dict) -> str:
    unassigned = [v for v in variables if v not in assignment]
    return min(unassigned, key=lambda v: len(domains[v]))


def _order_domain_values(var: str, assignment: dict,
                          domains: dict, neighbours: dict) -> list:
    def count_conflicts(value):
        return sum(
            1
            for nb in neighbours[var]
            if nb not in assignment and value in domains[nb]
        )
    return sorted(domains[var], key=count_conflicts)

def _is_consistent(var: str, value, assignment: dict,
                    neighbours: dict) -> bool:
    for nb in neighbours[var]:
        if nb in assignment and assignment[nb] == value:
            return False
    return True
