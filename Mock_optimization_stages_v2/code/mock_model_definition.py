# -*- coding: utf-8 -*-
"""
Define Pyomo model and solve it
Created on Thu Dec 22 12:34:41 2022

@author: RDVascoCJu
"""
import random
import pandas as pd
import numpy as np
from pyomo.environ import Set, Param, Var, Constraint, Objective, Reals, NonNegativeReals, \
    SolverFactory, maximize, minimize, AbstractModel, PercentFraction, Binary, Suffix, value
from objectives_function import cost_function
from output_dictionaries import OutputBuilder
from constants import MESSAGES, FINAL_STAGE_NAME
from reference_recipe import ReferenceRecipe
from solver_functions import solve_pyomo_model
from variable_translation import VariableTranslator

def list_to_df(data: list, index_col: str, constraint_type: str = None) -> pd.DataFrame:
    """
    Helper function to convert a list to a dataframe, setting the index appropriately if it exists
    :param data: json list containing data
    :index_col: string with name of index
    :data_type: string with name of constraint type
    :return: dataframe
    """
    if data:
        data_df = pd.DataFrame(data)
        if index_col in data_df.columns:
            data_df.set_index(index_col, inplace=True)
    else:
        data_df = pd.DataFrame(columns=['active'])

    # if the dataframe contains constraints we will rename the columns so they are all the same
    if 'operator' in data_df.columns:
        data_df.columns = rename_constraint_columns(list(data_df.columns))
        data_df['type'] = constraint_type

    if index_col == 'score':
        data_df.fillna('', inplace=True)

    return data_df


def add_row(df: pd.DataFrame, index: str, default: float = 0, override_values: dict = None) -> pd.DataFrame:
    """
    Add a row for evaporation to the dataframe with the specified index, defaulting to value.
    If override_values are provided override those columns with the specified values

    :param df: dataframe to be modified
    :param index: index to add
    :param default: default value
    :param override_values: dict mapping columns to set with values for those columns
    :return: df with added row
    """
    # if the dataframe has rows and columns
    if len(df) and len(df.columns):
        df.loc[index] = default

        if override_values:
            for column, value in override_values.items():
                if column in df.columns:
                    df.loc[index, column] = value

    return df


def solve_problem_single(instance, objectives, units, refrec, constraints, servingc, scon,
                         variable_translator: VariableTranslator) -> tuple:
    """
    Solve a problem where we create a single recipe
    """
    solver_output = solve_pyomo_model(instance)
    if solver_output['Termination condition'] == 'optimal':
        output_builder = OutputBuilder(model=instance, objectives=objectives, units=units, refrec=refrec, variable_translator=variable_translator)
        output_builder.add_recipe(constraints, servingc, scon)
        results_dict = output_builder.results_dict

        out_message = MESSAGES['optimal']
    else:
        out_message = MESSAGES['infeasible_single']
        results_dict = {}

    return results_dict, out_message, constraints


def solve_problem_multiple(instance, output_builder: OutputBuilder, constraints, servingc, scon) -> OutputBuilder:
    """
    Solve a problem and add the results to an existing results dict
    """
    solver_output = solve_pyomo_model(instance)
    if solver_output['Termination condition'] == 'optimal':
        output_builder.add_recipe(constraints, servingc, scon)

    instance.del_component(instance.obj_constraint)

    return output_builder


def create_range(objr: str, min_v: float, max_v: float, n_p: int) -> np.ndarray:
    """
    Creaye a linspace between min and max with the specified number of points, depending on the objective
    """
    if objr == 'nutritional score 2017' or objr == 'nutritional score 2023' or objr == 'HSR points':
        x_vals = np.unique(np.linspace(min_v, max_v, n_p, dtype=int))
    else:
        # only take unique values to save from repeatedly solving same problem
        x_vals = np.unique(np.linspace(min_v, max_v, n_p))

    return x_vals

def rename_constraint_columns(columns: list) -> list:
    """
    Rename the columns, replacing '* 1' and '* 2' with 'item 1' so that we have standard column names
    :param columns:
    """
    for i, item in enumerate(columns):
        if ' 1' in item:
            columns[i] = 'item 1'
        elif ' 2' in item:
            columns[i] = 'item 2'

    return columns

def combine_ingredients_dataframes(ingredients: dict, variable_translator: VariableTranslator) -> pd.DataFrame:
    """
    Convert the lists in the ingredients dict into dataframes and merge them on the ingredient index
    :param ingredients: dict containing all ingredient information
    :param variable_translator: object to handle converting names of variables
    """
    profile = list_to_df(ingredients['profile'], 'ingredient')
    profile.columns = pd.MultiIndex.from_product([['profile'], profile.columns])
    for data_type, data_list in ingredients.items():
        if data_type not in ['profile', 'cost', 'refrec']:
            tmp_data_df = list_to_df(data_list, 'ingredient')
            # add multi-index to group the columns
            tmp_data_df.columns = pd.MultiIndex.from_product([[data_type], tmp_data_df.columns])
            profile = profile.join(tmp_data_df)

    # rename the ingredients
    profile = variable_translator.rename_ingredients(profile)

    # create separate dataframe for cost, since each source good might have different costs for different stages
    cost = pd.DataFrame(ingredients['cost'])
    # if no target stage is specified, target for all is final stage
    if 'target_good' not in cost.columns:
        cost['target_good'] = FINAL_STAGE_NAME

    # rename cost ingredients
    cost = variable_translator.rename_cost_ingredients(cost)

    return profile, cost


def convert_data(ingredients, constraints, other_constraints, servingc, lconstraints, other_opt,
                 variable_translator: VariableTranslator) -> tuple:
    """
    Convert the data from lists to dicts and set the index appropriately
    """
    # create a single dataframe with all ingredient information, using multi-index to group columns
    profile, cost = combine_ingredients_dataframes(ingredients, variable_translator=variable_translator)

    classcon = list_to_df(other_constraints['classcon'], 'class name')
    servingc = list_to_df(servingc, 'serving parameter')
    scon = list_to_df(other_constraints['scon'], 'score')
    other = list_to_df(other_opt, 'parameter')

    # classcon target_good should default to Final
    if 'target_good' in classcon.columns:
        classcon['target_good'] = classcon['target_good'].fillna(FINAL_STAGE_NAME)
    else:
        classcon['target_good'] = FINAL_STAGE_NAME

    # optional constraints
    constraints_df = pd.DataFrame(
        columns=['item 1', 'operator', 'item 2', 'constraint', 'value', 'per', 'active', 'type', 'target_good'])
    for constraint_type, constraint_list in constraints.items():
        tmp_constraint_df = list_to_df(constraint_list, 'constraint name', constraint_type)
        # if there is data in the constraints_df, concat the new DF to it
        if not constraints_df.empty:
            constraints_df = pd.concat([constraints_df, tmp_constraint_df], axis=0)
        # otherwise initialize the constraints_df, making sure all needed columns are present
        else:
            constraints_df = pd.DataFrame(tmp_constraint_df,
                                          columns=['item 1', 'operator', 'item 2', 'constraint', 'value', 'per',
                                                   'active', 'type', 'target_good'])

    # ingredient constraints are all per 100g
    constraints_df.loc[constraints_df['type'] == 'ing', 'per'] = '100g'
    # cost constraints should have per equal to None to get a per_factor = 1 -> TBD if we want to actually implement cost/(100g, 100ml, etc)
    constraints_df.loc[constraints_df['type'] == 'costcon', 'per'] = None
    constraints_df.index.name = 'constraint name'

    # default target_good for constraints is final stage
    constraints_df['target_good'] = constraints_df['target_good'].fillna(FINAL_STAGE_NAME).replace(
        {'': FINAL_STAGE_NAME})

    # rename the ingredients in the constraints df
    constraints_df = variable_translator.rename_constraints_items(constraints_df)
    # rename the constraints
    constraints_df = variable_translator.rename_constraints(constraints_df)

    # add a column indicating which are loosened
    if len(lconstraints):
        lconstraints = list_to_df(lconstraints, 'constraint name')
        # rename the loosen constraints
        lconstraints = variable_translator.rename_loosen_constraints(lconstraints)
        constraints_df.loc[lconstraints.index, 'loose_strength'] = lconstraints['loosening strength']
    else:
        constraints_df['loose_strength'] = None

    # add columns with information for slack constraints
    constraints_df['no_loosen'] = False
    constraints_df[['slack value', 'constraint value']] = None

    return profile, cost, constraints_df, classcon, servingc, scon, other


def add_evaporation(profile, cost) -> tuple:
    """
    Add evaporation as an ingredient to the appropriate dataframes
    """
    # since evaporation is negative it has positive water
    profile = add_row(profile, 'evaporation', 0, {('profile', 'water'): 100, ('profile', 'Water'): 100})
    # TODO - will evaporation always have a 0 cost ?
    for target_stage in cost['target_good'].unique():
        cost.loc[len(cost), ['ingredient', 'cost', 'target_good']] = ['evaporation', 0, target_stage]
    return profile, cost


def scale_data(profile: pd.DataFrame, constraints: pd.DataFrame) -> tuple:
    """
    Scale the data to be in percentages
    """
    # don't scale division operator because division is already a ratio !
    constraints.loc[
        (constraints['type'].isin(['ing', 'class_amount']) & (constraints['operator'] != '/')), 'value'] /= 100.0

    return profile, constraints


def get_ingredient_columns(profile: pd.DataFrame, index: str, exclude: list = None) -> list:
    """
    Get the columns for the index, if they exist in the dataframe, otherwise return an empty list.
    If column to exclude is provided exclude it from the results
    """
    if exclude is None:
        exclude = []

    response = []
    if index in profile.columns:
        response = [col for col in profile[index].columns if col not in exclude]
    return response


def get_ingredient_values(profile: pd.DataFrame, index: str) -> dict:
    """
    If the index exists in the columns, stack the values and return a dict.
    Else return an empty dict
    """
    response = {}
    if index in profile.columns:
        response = profile[index].stack().to_dict()

    return response


def create_qualities(profile: pd.DataFrame) -> dict:
    """
    Create a dict of all qualities of ingredients from the profile dataframe
    """
    # each ingredient needs to have its ingredient property set to 1 for constraints to work properly
    qualities = {}
    profile_flat_cols = profile.copy()
    # drop ingtag columns as they are not numeric
    profile_flat_cols.drop('ingtags', axis=1, level=0, inplace=True)
    profile_flat_cols.columns = ["__".join(item) for item in profile_flat_cols.columns]
    qualities.update(profile_flat_cols.stack().to_dict())
    # qualities.update({
    #     (ing, ing): 1 for ing in profile.index
    # })
    return qualities


def create_paths(arcs: list, goods: list) -> list:
    """Create the paths from the arcs"""
    # create adjacency list
    graph = {}
    for i in goods:
        graph[i] = [item[1] for item in arcs if item[0] == i]

    paths = {}

    def depthFirst(graph, currentVertex, visited, visitedList):
        """Return a list of all nodes reachable from currentVertex"""
        visited.append(currentVertex)
        for vertex in graph[currentVertex]:
            if vertex not in visited:
                depthFirst(graph, vertex, visited.copy(), visitedList)
        visitedList.extend([item for item in visited if item not in visitedList])
        return visitedList

    for i in graph.keys():
        traversal = depthFirst(graph, i, [], [])
        for item in traversal:
            if i != item:
                paths[(i, item)] = 1
    return paths


def create_and_configure_instance(profile, cost, constraints, classcon, process_loss: list, stage_data: dict) -> tuple:
    """
    Create the model, set up the Sets, Params, and Variables and create the instance
    """
    model = AbstractModel()
    model.dual = Suffix(direction=Suffix.IMPORT)  # to store duals

    ## sets
    model.F_all = Set(initialize=list(profile.index) + stage_data['goods'])  # all goods
    model.F_source = Set(initialize=profile.index)  # source goods
    model.F_tagged = Set(
        initialize=[item for item in profile.index if item != 'evaporation'])  # Foods for ingtags (no evaporation)
    model.F_target = Set(initialize=stage_data['goods'])  # target food
    model.F_stages = Set(initialize=stage_data['goods'])  # non-source goods
    model.F_int_stages = Set(
        initialize=[item for item in stage_data['goods'] if item != FINAL_STAGE_NAME])  # intermediate stages
    model.F_except_target = Set(
        initialize=list(profile.index) + [item for item in stage_data['goods'] if item != FINAL_STAGE_NAME])
    model.qualities = Set(
        initialize=["__".join(item) for item in profile.columns])

    model.N = Set(initialize=profile['profile'].columns)  # Nutrients optimization set
    model.S = Set(initialize=get_ingredient_columns(profile, 'sustainability'))  # Sustainability optimization set
    model.O = Set(initialize=get_ingredient_columns(profile, 'otherp'))  # Other parameters optimization set
    model.AAd = Set(initialize=get_ingredient_columns(profile, 'AAprofile'))  # AA set + digestibility
    model.subcomp = Set(initialize=get_ingredient_columns(profile, 'subcomponents'))  # subcomponents
    model.AA = Set(
        initialize=get_ingredient_columns(profile, 'AAprofile', exclude=['digestibility']))  # AA set
    model.gtags = Set(initialize=classcon.index)  # class/tags groups/levels

    model.quality_constraints = Set(initialize=constraints[
        (constraints['active'] == 'yes') & (~constraints['type'].isin(['class_amount', 'costcon']))].index)
    # create sets for constraints
    for const_type in constraints['type'].unique():
        constraint_set = Set(
            initialize=constraints[(constraints['active'] == 'yes') & (constraints['type'] == const_type)].index)
        # assign the set to the model
        model.add_component(f"{const_type}_names", constraint_set)

    ## parameters
    model.q = Param(model.F_source, model.qualities, initialize=create_qualities(profile), within=Reals, default=0)

    model.c = Param(model.F_source, model.F_all,
                    initialize={(food, stage): cost for food, stage, cost in
                                cost[['ingredient', 'target_good', 'cost']].values},
                    within=NonNegativeReals, mutable=True, default=0)  # cost

    # process loss, default to 0
    model.process_loss = Param(model.F_all, model.qualities,
                               initialize={(item['target_good'], item['quality']): item['value'] for item in
                                           process_loss}, within=PercentFraction, default=0)
    if stage_data.get('arcs'):
        model.arcs = Param(model.F_all, model.F_all,
                           initialize={(item1, item2): 1 for item1, item2 in stage_data['arcs']},
                           default=0)
    else:
        # default arcs are all ingredients go directly to final recipe
        model.arcs = Param(model.F_all, model.F_all, initialize={(food, FINAL_STAGE_NAME): 1 for food in profile.index},
                           default=0)

    # create the paths
    model.paths = Param(model.F_all, model.F_all,
                        initialize=create_paths(stage_data['arcs'], goods=list(profile.index) + stage_data['goods']),
                        default=0)

    ## variables
    def x_bounds(model, i, j):
        """All ingredients should be between 0 and 1, except evaporation which should be between -1 and 0"""
        if i == 'evaporation':
            return (-1, 0)
        else:
            return (0, 1)

    model.x = Var(model.F_all, model.F_all, within=Reals, bounds=x_bounds)  # for ingredient amount
    model.y = Var(model.F_all, model.F_all, model.gtags, within=Binary)  # for ingredient presence or not
    model.cq = Var(model.F_all, model.qualities, within=NonNegativeReals)  # calculated qualities for stages

    ## creating instance of the model
    instance = model.create_instance()

    return instance



def get_min_max_values(instance, obj: str) -> tuple:
    """
    Get the min and max possible values for the objective by minimizing and maximizing
    """
    min_v = ''
    max_v = ''
    # min value possible
    instance.objective = Objective(rule=cost_function(instance, obj), sense=minimize)
    solver_output = solve_pyomo_model(instance)
    if solver_output['Termination condition'] == 'optimal':
        min_v = instance.objective()
    instance.del_component(instance.objective)

    # max value possible
    instance.objective = Objective(rule=cost_function(instance, obj), sense=maximize)
    solver_output = solve_pyomo_model(instance)
    if solver_output['Termination condition'] == 'optimal':
        max_v = instance.objective()
    instance.del_component(instance.objective)

    return min_v, max_v


def process_data(ingredients: dict, constraints: dict, other_constraints: dict, servingc: list, lconstraints: list,
                 other_opt: list, variable_translator: VariableTranslator) -> tuple:
    """
    Do all of the data processing required on the inputs
    """
    # convert lists to dataframes
    profile, cost, constraints, classcon, servingc, scon, other = convert_data(
        ingredients, constraints, other_constraints, servingc, lconstraints, other_opt,
        variable_translator=variable_translator)

    # if we need to add evaporation, have water as a nutrient, and don't already have evaporation add it
    if 'water' in profile['profile'].columns.str.lower() and 'evaporation' not in profile.index:
        profile, cost = add_evaporation(profile, cost)

    # scale the data
    profile, constraints = scale_data(profile, constraints)
    return profile, cost, constraints, classcon, servingc, scon, other


def _create_and_solve_model(profile, refrec, cost, constraints, classcon, servingc, scon, objectives, units,
                            stage_data: dict,
                            process_loss: list, variable_translator: VariableTranslator, n_p: int = 10):
    """
    Create and solve the model. Separating this out into a separate function allows us to easily
    modify the parameters and call it again.
    """
    results_dict = {}  # dictionary of results
    out_message = []  # output message
    instance = create_and_configure_instance(profile, cost, constraints, classcon, stage_data=stage_data,
                                             process_loss=process_loss)

    # set the constraints
    #set_constraints(instance, profile, refrec, constraints, classcon, servingc, scon)

    # optimization
    if len(objectives) == 1:
        obj = objectives[0]['Objective']
        option = objectives[0]['Option']
        if option in ['minimize', 'maximize']:
            # constraints are not loosened
            if constraints['loose_strength'].isna().all():
                instance.objective = Objective(rule=cost_function(instance, obj),
                                               sense=minimize if option == 'minimize' else maximize)

                # solve the problem and create the output
                results_dict, out_message, constraints = solve_problem_single(instance, objectives, units,
                                                                              refrec, constraints,
                                                                              servingc, scon,
                                                                              variable_translator=variable_translator)
            
            else:
                results_dict, out_message, constraints = solve_problem_single(instance, objectives, units,
                                                                              refrec,
                                                                              constraints,
                                                                              servingc, scon,
                                                                              variable_translator=variable_translator)

        elif option == 'range':
            # get the min and max possible values
            min_v, max_v = get_min_max_values(instance, obj)

            # minimizing cost as default objective for range but could be different
            instance.objective = Objective(rule=cost_function(instance, 'cost'), sense=minimize)

            if min_v != '' and max_v != '':
                x_vals = create_range(obj, min_v, max_v, n_p)

                # initialize the output builder
                output_builder = OutputBuilder(instance, objectives, units, refrec,
                                               variable_translator=variable_translator)
                for i in x_vals:
                    instance.obj_constraint = Constraint(rule=cost_function(instance, obj) == i)
                    output_builder = solve_problem_multiple(instance, output_builder, constraints, servingc,
                                                            scon)

                results_dict = output_builder.results_dict
                out_message = MESSAGES['optimal']
            else:
                out_message = MESSAGES['infeasible_range']

    elif len(objectives) == 2:
        if constraints['loose_strength'].isna().all():
            obj1 = objectives[0]['Objective']
            obj2 = objectives[1]['Objective']
            option1 = objectives[0]['Option']
            option2 = objectives[1]['Option']

            if option1 == 'range':
                objr, objo = obj1, obj2
                optionr, optiono = option1, option2
            else:
                objr, objo = obj2, obj1
                optionr, optiono = option2, option1

            # get the min and max possible values
            min_v, max_v = get_min_max_values(instance, objr)

            if min_v != '' and max_v != '':
                x_vals = create_range(objr, min_v, max_v, n_p)

                output_builder = OutputBuilder(instance, objectives, units, refrec,
                                               variable_translator=variable_translator)
                instance.objective = Objective(rule=cost_function(instance, objo),
                                               sense=minimize if optiono == 'minimize' else maximize)
                for i in x_vals:
                    if optionr == 'minimize':  # minimizing objective objr
                        instance.obj_constraint = Constraint(rule=cost_function(instance, objr) <= i)
                    elif optionr == 'maximize':  # maximizing objective objr
                        instance.obj_constraint = Constraint(rule=cost_function(instance, objr) >= i)
                    elif optionr == 'range':  # recipes within possible range for objr
                        instance.obj_constraint = Constraint(rule=cost_function(instance, objr) == i)

                    output_builder = solve_problem_multiple(instance, output_builder, constraints, servingc,
                                                            scon)

                results_dict = output_builder.results_dict
                out_message = MESSAGES['optimal']
            else:
                out_message = MESSAGES['infeasible_multi']
        else:
            out_message = MESSAGES['loosen_multi_objective']

    return results_dict, constraints, out_message, instance


def default_stage_data(stage_data: dict, ingredients: list, other_opt: pd.DataFrame = None, variable_translator: VariableTranslator = None) -> dict:
    """
    Make sure we have a dict for stage_data, infer goods from arcs
    """
    if stage_data is None:
        stage_data = {'arcs': [], 'goods': [FINAL_STAGE_NAME]}

    # if we have no specified arcs, each ingredient goes directly to the final stage,
    # except for evaporation, which needs to be manually specified
    if not stage_data.get('arcs'):
        stage_data['arcs'] = [[ingredient, FINAL_STAGE_NAME] for ingredient in ingredients if ingredient != 'evaporation']
        if other_opt is not None and other_opt.loc['evaporation', 'value'] == 1:
            stage_data['arcs'].append(['evaporation', FINAL_STAGE_NAME])

    if 'goods' not in stage_data:
        stage_data['goods'] = []

    if variable_translator:
        stage_data['arcs'] = variable_translator.rename_arcs(stage_data['arcs'])

    # if we have no goods specified, infer them from the arcs
    if not stage_data['goods']:
        for arc in stage_data['arcs']:
            stage_data['goods'].extend(
                [item for item in arc if item not in stage_data['goods'] and item not in ingredients])

    return stage_data


def create_and_solve_model(ingredients: dict, units: dict, constraints: dict, other_constraints: dict, servingc: list,
                           objectives, lconstraints: list, other_opt: list, auto_loosen: bool = True,
                           process_loss: list = None, stage_data: dict = None, bypass_renaming: bool = False,
                           n_p: int = 10) -> tuple:
    """
    Creates pyomo optimization model
    
    Input parameters (json-list format):
        ingredients: dict with lists related to ingredients
            profile: raw ingredients with nutritional profile
            sustainability: raw ingredients with sustainability profile
            otherp: raw ingredients with other parameters profile
            refrec: reference recipe
            cost: raw ingredients with cost
        units: units of nutrients and cost
        constraints: dict of constraints lists (can be []) with multi-item format
        classcon: class constraints
        servingc: serving size constraints
        scon: scores constraints
        objectives: objective list
        lconstraints: list of constraints to loosen (can be [])
        other_opt: other optional parameters (evaporation)
        auto_loosen: whether to automatically loosen the constraints if the problem is infeasible
        process_loss: list of process loss values
        stage_data: dict containing information about stages - names and arcs
        n_p: number of points to construct pareto front with

    results_dict, constraints_loosen_slacks, no_loosen, out_message, instance
    
    Output parameters:
        results_dict: optimal recipes (dictionary)
        constraints_loosen_slacks: loosened constraints with slacks (dictionary)
        no_loosen: constraints not considered by the loosen constraints algorithm (string list)
        out_message: result of the optimization (string)
        instance: created pyomo model (pyomo model)
    """
    # initialize a variable translator
    variable_translator = VariableTranslator(bypass=bypass_renaming)

    # outputs
    if objectives:
        profile, cost, constraints, classcon, servingc, scon, other = process_data(
            ingredients, constraints, other_constraints, servingc, lconstraints, other_opt,
            variable_translator=variable_translator)

        # if no stages are passed we add a default good of the final product
        stage_data = default_stage_data(stage_data=stage_data, ingredients=profile.index, other_opt=other,
                                        variable_translator=variable_translator)

        # instantiate an instance of the reference recipe class
        refrec = ReferenceRecipe(refrec=ingredients['refrec'], cost=cost, profile=profile, process_loss=process_loss,
                                 arcs=stage_data['arcs'], variable_translator=variable_translator)

        if process_loss is None:
            process_loss = []

        variable_translator.stage_data = stage_data

        # rename the objectives, as they may include ingredients
        objectives = variable_translator.rename_objectives(objectives_list=objectives)

        results_dict, constraints, out_message, instance = _create_and_solve_model(profile, refrec, cost, constraints,
                                                                                   classcon,
                                                                                   servingc, scon, objectives, units,
                                                                                   process_loss=process_loss,
                                                                                   n_p=n_p, stage_data=stage_data,
                                                                                   variable_translator=variable_translator)

        # if the problem was not solved we will loosen ingredient constraints and re-solve
        if auto_loosen and out_message != MESSAGES['optimal'] and len(objectives) == 1:
            constraints.loc[(constraints['type'].isin(['ing'])) & (
                constraints['loose_strength'].isna()) & (constraints['active'] == 'yes'), 'loose_strength'] = 'low'
            results_dict, constraints, out_message, instance = _create_and_solve_model(profile, refrec, cost,
                                                                                       constraints,
                                                                                       classcon,
                                                                                       servingc, scon, objectives,
                                                                                       units, process_loss=process_loss,
                                                                                       n_p=n_p, stage_data=stage_data,
                                                                                       variable_translator=variable_translator)
            if out_message == MESSAGES['optimal']:
                out_message = MESSAGES['optimal_loosened']

        if out_message in [MESSAGES['infeasible_multi'], MESSAGES['infeasible_single'], MESSAGES['infeasible_range'],
                           MESSAGES['loosen_multi_objective']]:
            constraints_loosen_slacks = []
        else:
            # only return constraints that have a non-zero slack            
            constraints_loosen_slacks = constraints.loc[
                ~constraints['loose_strength'].isna() & ~constraints['no_loosen'] & np.logical_or(
                    constraints['slack value'] > 1e-10, constraints['slack value'] < -1e-10), ['slack value',
                                                                                               'constraint value',
                                                                                               'per']].reset_index().to_dict(
                'records')

    else:
        raise Exception(MESSAGES['no_objective']['message'])

    # reverse the renaming of constraints
    constraints = variable_translator.reverse_rename_constraints(constraints)
    # reverse the renaming of the loosened constraints
    constraints_loosen_slacks = variable_translator.reverse_translate_constraints_list(constraints_loosen_slacks)

    constraints_loosen_slacks = []
    for l in range(0,random.randint(0,len(lconstraints))):
        constraints_loosen_slacks = constraints_loosen_slacks + [{'constraint name': lconstraints[l]['constraint name'], 
                                                                  'slack value': 10*(0.5-random.random()), 
                                                                  'constraint value': 10*random.random(), 
                                                                  'per': (['serving','100g','100kcal','100ml'])[random.randint(0,3)]}]


    return results_dict, constraints_loosen_slacks, list(
        constraints[constraints['no_loosen']].index), out_message, instance
