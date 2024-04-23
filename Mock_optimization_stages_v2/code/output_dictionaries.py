"""
This module contains create the dictionaries with the optimization results
"""
import random
import pandas as pd
import numpy as np
from pyomo.environ import value
from objectives_function import cost_function, cost_function_ref
from reference_recipe import ReferenceRecipe
from constants import FINAL_STAGE_NAME

def get_per_factor_df(model, df: pd.DataFrame, servingc: pd.DataFrame, solved: bool) -> pd.DataFrame:
    """
    Return a dataframe with the list of the constraints in df with the factor
    converting those constraints to per 100g
    :param model: the model
    :param df: dataframe of constraints
    :param servingc: dataframe of serving sizes
    :param solved: whether the problem has been solved
    :return:
    """
    # value scaling-factors for 'per' choices
    per_factor = pd.DataFrame(columns=['factor'], index=df.index)
    for i in per_factor.index:
        if df.loc[i, 'per'] in ['100g', None]:  # we use None for cost constraints
            per_factor.loc[i, 'factor'] = 1.0
        elif df.loc[i, 'per'] == 'serving':
            per_factor.loc[i, 'factor'] = (100.0 / servingc.loc['sps_as_sold_g', 'value'])
        elif df.loc[i, 'per'] == '100ml':
            if servingc.loc['dp_as_consumed_gml', 'value'] in ['', None]:  # default is 1
                density = 1
            else:
                density = servingc.loc['dp_as_consumed_gml', 'value']

            per_factor.loc[i, 'factor'] = servingc.loc['sps_as_consummed_g', 'value'] / (servingc.loc[
                                                                                             'sps_as_sold_g', 'value'] * density)

        elif model is not None and df.loc[i, 'per'] == '100kcal':
            if 'energy' in model.N:
                energy_name = 'energy'
            elif 'Energy' in model.N:
                energy_name = 'Energy'
            elif 'calories' in model.N:
                energy_name = 'calories'
            elif 'Calories' in model.N:
                energy_name = 'Calories'
            else:
                raise ValueError('No energy found !')

            target_good = df.loc[i, 'target_good']
            # if the model is not passed skip this block, to allow for testing without a model
            if not solved:
                energy = model.cq[target_good, f"profile__{energy_name}"]
            else:
                energy = value(model.cq[target_good, f"profile__{energy_name}"])
            per_factor.loc[i, 'factor'] = 0.01 * energy  # assuming energy in kcal/100g and nutrient in per /100g units

    return per_factor


class OutputBuilder:
    """Class to create and return output dictionaries"""

    def __init__(self, model, objectives: pd.DataFrame, units: dict, refrec: ReferenceRecipe,
                 variable_translator, start_idx: int = 1) -> None:
        """
        :param model: pyomo model
        :param objectives: dataframe with objectives
        :param units: dict with units for nutrients
        :param profile: dataframe with reference recipe
        :param start_idx: integer with which to start indexing recipes
        """
        self.model = model
        self.objectives = objectives
        self.units = units
        self.refrec = refrec
        self.start_idx = start_idx
        self.variable_translator = variable_translator
        # initialize the results_dict
        self.results_dict = self.output_dict()

    def output_dict(self) -> None:
        """
        Create and return an output dictionary
        """
        results_dict = {'objective': {}, 'recipes': {}}
        for obj_idx, objective in enumerate(self.objectives, start=self.start_idx):
            objective_name = self.variable_translator.reverse_translate(objective['Objective'])
            results_dict['objective'][obj_idx] = {}
            results_dict['objective'][obj_idx]['name'] = objective_name
            results_dict['objective'][obj_idx]['unit'] = self.units.get(objective_name)
            results_dict['objective'][obj_idx]['reference value'] = value(
                cost_function_ref(self.model, self.refrec, objective['Objective'])) if objective[
                                                                                           'Objective'] not in self.model.F_all else 100 * value(
                cost_function_ref(self.model, self.refrec, objective['Objective']))

        return results_dict

    @staticmethod
    def initialize_recipe_values(data: dict) -> dict:
        """
        Initialize the slack bounds in the dict
        :param data: dict to add slack bounds to
        :return:
        """
        for key in ['lbound', 'ubound', 'lslack', 'uslack']:
            data[key] = np.nan
        return data

    @staticmethod
    def get_min_max_values(eqv: pd.DataFrame, single_constraint: pd.DataFrame, model_field) -> tuple:
        """
        Get the min and max values for the appropriate constraint
        :param eqv: dataframe containing equal constraints
        :param single_constraint: dataframe all relevant constraints
        :param model_field: the field of the model containing the constraints
        """
        if eqv.empty:
            smaxv = single_constraint[single_constraint.loc[:, 'constraint'] == '<='].loc[:, 'value']
            sminv = single_constraint[single_constraint.loc[:, 'constraint'] == '>='].loc[:, 'value']

            if smaxv.empty:
                maxv = np.nan
                us = np.nan
            else:
                pmaxv = smaxv.argmin()  # min val position
                maxv = smaxv.values[pmaxv]  # min val -> actual max value of the constraint
                us = model_field[smaxv.index[pmaxv]].uslack()  # uslack for constraint name

            if sminv.empty:
                minv = np.nan
                ls = np.nan
            else:
                pminv = sminv.argmax()  # max val position
                minv = sminv.values[pminv]  # max val -> actual min value of the constraint
                ls = model_field[sminv.index[pminv]].lslack()  # lslack for constraint name
        else:
            maxv = eqv.values[0]
            minv = eqv.values[0]
            us = 0
            ls = 0

        return minv, maxv, ls, us

    @staticmethod
    def set_recipe_values(data: dict, minv: float, maxv: float, ls: float, us: float, multiplier: int = 1) -> dict:
        """
        Set the recipe values in the provided data dict
        :param data: dict to add values to
        :param minv: min value
        :param maxv: max value
        :param ls: lower slack
        :param us: upper slack
        :param multiplier: multiplier to multiply values by
        :return:
        """
        data['lbound'] = multiplier * minv
        data['ubound'] = multiplier * maxv
        data['lslack'] = multiplier * ls
        data['uslack'] = multiplier * us
        return data

    @staticmethod
    def extract_constraints(constraint_df: pd.DataFrame, per_factor_df: pd.DataFrame, column: str,
                            constraint_name: str) -> tuple:
        """
        Extract the constraints for the specified constraint and return one dataframe with the active constraints
        and one with the active equality constraints
        """
        single_constraint_df = constraint_df.loc[
            (constraint_df[f'{column} 1'] == constraint_name) & (constraint_df[f'{column} 2'] == '') & (
                    constraint_df['active'] == 'yes')].copy()
        # scale the value in the dataframe to account for serving size
        if per_factor_df is not None:
            single_constraint_df['value'] = single_constraint_df.loc[single_constraint_df.index, 'value'] * \
                                            per_factor_df.loc[
                                                single_constraint_df.index, 'value']  # rescaling the value to make it in per 100g units
        # extract tge constraints that are for equalities
        eqv_df = single_constraint_df.loc[single_constraint_df['constraint'] == '=', 'value']

        return single_constraint_df, eqv_df

    @property
    def recipe_idx(self) -> int:
        """Get the index for which to add a recipe, to avoid having to keep track of this externally"""
        # if there are no recipes we use the start_idx
        if len(self.results_dict['recipes']) == 0:
            idx = self.start_idx
        # else we add the number of recipes currently present to the start_idx
        else:
            idx = len(self.results_dict['recipes']) + self.start_idx
        return idx

    def add_objective(self, recipe: dict) -> dict:
        """
        Add the objectives to the recipe dict
        :param recipe: dict containing recipe
        """
        for objective_dict in self.objectives:
            objective = objective_dict['Objective']
            objective_name = self.variable_translator.reverse_translate(objective)
            if objective_name == 'pdcaas':  
                recipe[objective_name] = random.random()
            else:
                recipe[objective_name] = value(
                    cost_function(self.model, objective)) if objective not in self.model.F_all else 100 * value(
                    cost_function(self.model, objective))
        recipe['optimum_cost'] = value(cost_function(self.model, 'cost'))
        recipe['reference_cost'] = value(cost_function_ref(self.model, self.refrec, 'cost'))
        recipe['unit_cost'] = self.units.get('cost')
        return recipe

    def create_per_factor_df(self, constraint_df: pd.DataFrame, servingc: pd.DataFrame) -> pd.DataFrame:
        """
        Create the per factor df for the provided constraints, set the columns and make sure the value is a float
        :param constraint_df: dataframe with constraints
        :param servingc: dataframe with serving information
        """
        per_factor = get_per_factor_df(self.model, constraint_df, servingc, True)
        per_factor.columns = ['value']
        per_factor['value'] = per_factor['value'].astype(float)

        return per_factor

    def add_values_to_recipe(self, model_set, model_constraint_field, constraint_df, servingc,
                             col_name, stage: str = FINAL_STAGE_NAME) -> dict:
        """
        Create a recipe dict
        :param model_set: the Set we need to loop through
        :param model_constraint_field: the relevant constraint
        :param constraint_df: the dataframe with the constraints
        :param servingc: the dataframe containing serving information
        :param col_name: the column name for the constraints
        """
        recipe = {}
        per_factor_df = self.create_per_factor_df(constraint_df, servingc)
        for j in model_set:
            recipe[j] = {}

            # adding nutrients amounts
            recipe[j]['optimum'] = value(self.model.cq[stage, f"{model_constraint_field}__{j}"] * sum(
                self.model.x[i, stage] for i in self.model.F_all if value(self.model.arcs[i, stage]) != 0))
            recipe[j]['reference'] = self.refrec.quality(f"{model_constraint_field}__{j}", stage)

            # setting default values to nan
            recipe[j] = self.initialize_recipe_values(recipe[j])

            if not constraint_df.empty:
                minv = 0
                maxv = 1
                ls = 0
                us = 0 

                recipe[j] = self.set_recipe_values(recipe[j], minv, maxv, ls, us, multiplier=1)

        return recipe

    def _add_nutriscore_data(self, recipe: dict, scon: pd.DataFrame) -> dict:
        """
        Add nutriscore data to the recipe dict
        :param recipe: dict containing recipe information
        :param scon: dataframe with score constraints
        """
        if 'nutriscore_2017' in scon.index:
            NS = scon.loc['nutriscore_2017', 'min value']
            case = scon.loc['nutriscore_2017', 'type']
            version = 'nutriscore_2017'
        elif 'nutriscore_2023' in scon.index:
            NS = scon.loc['nutriscore_2023', 'min value']
            case = scon.loc['nutriscore_2023', 'type']
            version = 'nutriscore_2023'
        else:
            NS = ''
            case = ''

        if NS not in ['', 'Not. App.', None] and case not in ['', None]:
            recipe['nutriscore data']['score'] = {}
            recipe['nutriscore data']['NutriScore'] = {}
            recipe['nutriscore data']['score_break_down'] = {}
            recipe['nutriscore data']['version'] = version

            # optimum values
            recipe['nutriscore data']['score']['optimum'] = random.randint(-10,20)
            recipe['nutriscore data']['NutriScore']['optimum'] = (['A','B','C','D','E'])[random.randint(0,4)]
            recipe['nutriscore data']['score_break_down']['optimum'] = {}
            for i in ['sugars', 'protein', 'fiber', 'sodium', 'sfa', 'energy', 'fvpno_eff']:
                recipe['nutriscore data']['score_break_down']['optimum'][i] = {'value': 100*random.random(),
                                                                               'score': random.randint(0,20)}

            recipe['nutriscore data']['score']['reference'] = random.randint(-10,20)
            recipe['nutriscore data']['NutriScore']['reference'] = (['A','B','C','D','E'])[random.randint(0,4)]
            recipe['nutriscore data']['score_break_down']['reference'] = {}
            for i in ['sugars', 'protein', 'fiber', 'sodium', 'sfa', 'energy', 'fvpno_eff']:
                recipe['nutriscore data']['score_break_down']['reference'][i] = {'value': 100*random.random(),
                                                                                 'score': random.randint(0,20)}

        return recipe

    def _add_HSR_data(self, recipe: dict, scon: pd.DataFrame) -> dict:
        """
        Add HSR data to the recipe dict
        :param recipe: dict containing recipe information
        :param scon: dataframe with score constraints
        """
        HSR = scon.loc['HSR', 'min value']
        case = scon.loc['HSR', 'type']

        if HSR not in ['', 'Not. App.', None] and case not in ['', None]:
            recipe['HSR']['points'] = {}
            recipe['HSR']['score'] = {}
            recipe['HSR']['score_break_down'] = {}

            recipe['HSR']['points']['optimum'] = random.randint(-10,20)
            recipe['HSR']['score']['optimum'] = random.randint(1,10)/2
            recipe['HSR']['score_break_down']['optimum'] = {}
            for i in ['sugars', 'protein', 'fiber', 'sodium', 'sfa', 'energy', 'fv_c', 'fvnl_nc']:
                recipe['HSR']['score_break_down']['optimum'][i] = {'value': 100*random.random(),
                                                                   'score': random.randint(0,20)}

            recipe['HSR']['points']['reference'] = random.randint(-10,20)
            recipe['HSR']['score']['reference'] = random.randint(1,10)/2
            recipe['HSR']['score_break_down']['reference'] = {}
            for i in ['sugars', 'protein', 'fiber', 'sodium', 'sfa', 'energy', 'fv_c', 'fvnl_nc']:
                recipe['HSR']['score_break_down']['reference'][i] = {'value': 100*random.random(),
                                                                     'score': random.randint(0,20)}

        return recipe

    def _add_recipe(self, constraints: pd.DataFrame, servingc: pd.DataFrame, scon: pd.DataFrame,
                    stage: str = FINAL_STAGE_NAME) -> None:
        """
        Create a results dict for a single recipe and add it to the results
        :param constraints: dataframe with all constraints
        :param servingc: dataframe with serving information
        :param scon: nutrition score constraints
        :param stage: which stage the recipe is being added for
        """
        # initialize the recipe dict with the necessary keys
        recipe = {'ingredients': {}, 'nutrients': {}, 'sustainability': {}, 'other parameters': {},
                  'nutriscore data': {}, 'HSR': {}, 'PDCAAS data': {}, 'subcomponents': {}, 'Iumami': {}}

        # only add objective to final stage, for other stages it won't be correct
        if stage == FINAL_STAGE_NAME:
            recipe = self.add_objective(recipe)

        ## adding ingredients data
        for i in self.model.F_except_target:
            if value(self.model.arcs[i, stage]) != 0:
                ingr_name = self.variable_translator.reverse_translate(i)
                recipe['ingredients'][ingr_name] = {}

                # if the stage is neither the final stage nor a source ingredient we need to add a sub-recipe dict
                if i not in self.model.F_source and i != FINAL_STAGE_NAME:
                    recipe['ingredients'][ingr_name]['recipe'] = self._add_recipe(constraints, servingc, scon, stage=i)

                # adding ingredient amounts
                recipe['ingredients'][ingr_name]['optimum'] = 100 * value(self.model.x[i, stage])
                if i in self.refrec.goods:
                    recipe['ingredients'][ingr_name]['reference'] = 100 * self.refrec.value(i, stage)

                # adding ingredient costs
                if i in self.model.F_source:
                    # if i is a source ingredient we multiply the cost by the amount in this stage
                    recipe['ingredients'][ingr_name]['optimum_cost'] = value(
                        self.model.c[i, stage] * self.model.x[i, stage])
                else:
                    # else i is a stage we need to sum the cost of the ingredients in this stage
                    recipe['ingredients'][ingr_name]['optimum_cost'] = value(sum(
                        self.model.c[s, i] * self.model.x[s, i] for s in self.model.F_source if
                        value(self.model.arcs[s, i]) != 0))
                recipe['ingredients'][ingr_name]['reference_cost'] = self.refrec.cost_value(i, stage=stage)

                # setting default values to nan
                recipe['ingredients'][ingr_name] = self.initialize_recipe_values(recipe['ingredients'][ingr_name])

                if (constraints['type'] == 'ing').any():
                    minv = 0
                    maxv = 1
                    ls = 0
                    us = 0
                    recipe['ingredients'][ingr_name] = self.set_recipe_values(recipe['ingredients'][ingr_name], minv,
                                                                              maxv, ls, us,
                                                                              multiplier=100)

        # adding nutrient data
        recipe['nutrients'] = self.add_values_to_recipe(model_set=self.model.N,
                                                        model_constraint_field='profile',
                                                        constraint_df=constraints[constraints['type'] == 'profile'],
                                                        servingc=servingc, col_name='item', stage=stage)

        ## adding sustainability data
        recipe['sustainability'] = self.add_values_to_recipe(model_set=self.model.S,
                                                             model_constraint_field='sustainability',
                                                             constraint_df=constraints[
                                                                 constraints['type'] == 'sustainability'],
                                                             servingc=servingc,
                                                             col_name='item', stage=stage)

        ## adding other parameters data
        recipe['other parameters'] = self.add_values_to_recipe(model_set=self.model.O,
                                                               model_constraint_field='otherp',
                                                               constraint_df=constraints[
                                                                   constraints['type'] == 'otherp'],
                                                               servingc=servingc, col_name='item', stage=stage)

        ## add subcomponents
        recipe['subcomponents'] = self.add_values_to_recipe(model_set=self.model.subcomp,
                                                            model_constraint_field='subcomponents',
                                                            constraint_df=constraints[
                                                                constraints['type'] == 'subcomponents'],
                                                            servingc=servingc, col_name='item', stage=stage)

        ## adding nutriscore data
        recipe = self._add_nutriscore_data(recipe, scon)

        ## adding HSR data
        recipe = self._add_HSR_data(recipe, scon)

        ## adding PDCAAS data
        if scon.loc['PDCAAS', 'min value'] not in ['', None, 'Not. App.'] and scon.loc['PDCAAS', 'type'] not in ['',
                                                                                                                 None]:
            recipe['PDCAAS data']['reference'] = random.random()
            recipe['PDCAAS data']['optimum'] = random.random()
            recipe['PDCAAS data']['AA_breakdown'] = {}
            recipe['PDCAAS data']['AA_breakdown']['optimum'] = {}

            # getting the AA contribution to optimal recipe
            df_AAC = pd.DataFrame(index=[i for i in self.model.F_source]+['pattern'], columns=[i for i in self.model.AA])
            for i in df_AAC.index:
                if i != 'pattern':
                    for j in df_AAC.columns:
                        df_AAC.loc[i,j] = 100*random.random()
                else:
                    for j in df_AAC.columns:
                        df_AAC.loc[i,j] = 100*random.random()

            # translating ing names
            for i in self.model.F_source:
                ingr_name = self.variable_translator.reverse_translate(i)
                df_AAC.rename(index={i: ingr_name}, inplace=True)
            # storing values in dictionary
            for j in df_AAC.columns:
                recipe['PDCAAS data']['AA_breakdown']['optimum'][j] = {}
                for i in df_AAC.index:
                    recipe['PDCAAS data']['AA_breakdown']['optimum'][j][i] = df_AAC.loc[i, j]

        ## adding umami intensity if umami enhancers are available in profile
        if {i for i in self.model.N} & set(['MSG', 'kWGS', 'cWGH', 'YE standard light', 'CSB 110', 'IMP', 'Ribotide (I+G)', 'GMP', 'Umamex III', 'Himax IG20P', 'YE 2012', 'CSB 210', 'HPP', 'YE 2020', 'YE Maxarome XF']):
            recipe['Iumami']['reference'] = 100*random.random()
            recipe['Iumami']['optimum'] = 100*random.random()

        return recipe

    def add_recipe(self, constraints: pd.DataFrame, servingc: pd.DataFrame, scon: pd.DataFrame,
                   stage: str = FINAL_STAGE_NAME) -> None:
        recipe = self._add_recipe(constraints, servingc, scon, stage)
        self.results_dict['recipes'][self.recipe_idx] = recipe