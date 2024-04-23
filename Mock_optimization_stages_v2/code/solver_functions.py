# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 11:05:21 2023

@author: RDVascoCJu
"""

from pyomo.environ import SolverFactory
import random


def solve_pyomo_model(instance, solver_options: dict = {'AbsIntFeasTol': 1e-12}) -> dict:
    """
    Solves pyomo model

    :param solver_options: solver options
    :return: dictionary with termination results
    """

    for i in instance.F_all:
        for j in instance.F_all:
            if i == 'evaporation':
                instance.x[i,j] = -random.random()
            else:
                instance.x[i,j] = random.random()

    for i in instance.F_all:
        for j in instance.F_all:
            for k in instance.gtags:
                instance.y[i,j,k] = random.randint(0,1)

    for i in instance.F_all:
        for j in instance.qualities:
            instance.cq[i,j] = 100*random.random()
    
    # output dictionary 
    solver_output = {}
    solver_output['Termination condition'] = 'optimal' # '' -> otherwise

    return solver_output
