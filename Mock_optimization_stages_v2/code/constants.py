"""
File to contain constants referenced in other files

author: Eric A Scuccimarra (ericantoine.scuccimarra@rd.nestle.com)
"""

#M = 10

INFINITY = float('inf')

MESSAGES = {
    'no_objective': {'message': 'Please select at least one objective', 'status': 'danger'},
    'optimal': {'message': 'Optimal solution found!', 'status': 'success'},
    'optimal_loosened': {'message': 'Problem was infeasible, but solved with loosened active ingredient constraints', 'status': 'info'},
    'infeasible_multi': {'message': 'Problem infeasible! Set a single objective and loosen constraints to make it feasible', 'status': 'danger'},
    'infeasible_single': {'message': 'No optimal solution found. Try loosening constraints', 'status': 'danger'},
    'infeasible_range': {'message' : 'Problem infeasible! Set either minimize or maximize and loosen constraints to make it feasible', 'status': 'danger'},
    'loosen_multi_objective': {'message': 'The loosen constraints feature only supported for one objective', 'status': 'danger'},
}

FINAL_STAGE_NAME = 'Final'