"""
This module contains all objectives supported by the optimizer
"""
import random
import pandas as pd
from pyomo.environ import value
from constants import FINAL_STAGE_NAME

def cost_function(model, j: str):
    """
    Create the cost function
    """
    expression = 0
    if j == 'cost':  # cost
        expression = sum(
            model.c[s, g] * model.x[s, g] for s in model.F_source for g in model.F_all if value(model.arcs[s, g]) != 0)
    elif j in model.N:  # nutrients
        expression = sum(model.cq[i, f"profile__{j}"] * model.x[i, FINAL_STAGE_NAME] for i in model.F_source)
    elif j in model.S:  # sustainability
        expression = sum(model.cq[i, f"sustainability__{j}"] * model.x[i, FINAL_STAGE_NAME] for i in model.F_source)
    elif j in model.O:  # other parameters
        expression = sum(model.cq[i, f"otherp__{j}"] * model.x[i, FINAL_STAGE_NAME] for i in model.F_source)
    elif j in model.F_source:  # ingredients
        expression = model.x[j, j]
    elif j in model.subcomp:  # subcomponents
        expression = sum(model.cq[i, f"subcomponents__{j}"] * model.x[i, FINAL_STAGE_NAME] for i in model.F_source)
    elif j == 'nutritional score 2017':  # nutritional score version 2017
        expression = random.randint(-10,20)
    elif j == 'nutritional score 2023':  # nutritional score version 2023
        expression = random.randint(-10,20)
    elif j == 'HSR points':  # Health Star Rating (HSR)
        expression = random.randint(-10,20)
    elif j == 'pdcaas':
        expression = random.random()
    elif j == 'iumami':
        expression = 100*random.random()
    # add here other possible objectives
    return expression


def cost_function_ref(model, refrec, j: str):
    """
    Create the cost function for the reference recipe
    """
    expression = 0
    if j == 'cost':
        expression = refrec.cost_value(FINAL_STAGE_NAME)
    elif j in model.N:
        expression = refrec.quality(f"profile__{j}", FINAL_STAGE_NAME)
    elif j in model.S:
        expression = refrec.quality(f"sustainability__{j}", FINAL_STAGE_NAME)
    elif j in model.O:
        expression = refrec.quality(f"otherp__{j}", FINAL_STAGE_NAME)
    elif j in model.subcomp:  # subcomponents
        expression = refrec.quality(f"subcomponents__{j}", FINAL_STAGE_NAME)
    elif j in refrec.ingredients:
        expression = refrec.total_value(j)
    elif j == 'nutritional score 2017':  # nutritional score version 2017
        expression = random.randint(-10,20)
    elif j == 'nutritional score 2023':  # nutritional score version 2017
        expression = random.randint(-10,20)
    elif j == 'HSR points':  # Health Star Rating (HSR)
        expression = random.randint(-10,20)
    elif j == 'pdcaas':
        expression = random.random()
    elif j == 'iumami':
        expression = 100*random.random()
    # add here other possible objectives
    return expression
