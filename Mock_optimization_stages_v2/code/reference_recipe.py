# -*- coding: utf-8 -*-
"""
Class to contain and manipulate reference recipe
Created on Mon Sept 4, 2023

@author: RDScucciEr
"""
import pandas as pd
from constants import FINAL_STAGE_NAME


class ReferenceRecipe:
    def __init__(self, refrec: list, cost: pd.DataFrame, profile: pd.DataFrame, process_loss: list = None,
                 arcs: list = None, variable_translator=None) -> None:

        # rename the refrec
        refrec = variable_translator.rename_refrec(refrec)

        # index is actual ingredients, the reference recipe may contain non-source goods
        self.ingredients = list(profile.index)
        refrec = self._create_refrec_df(arcs, refrec)

        # save all goods present in the reference recipe
        self.goods = refrec['ingredient'].unique()
        self.refrec = self._add_costs(refrec, cost)
        self.scale_values(by=100)
        self.cq = self._calculate_qualities(profile, self.refrec, process_loss)

    @classmethod
    def _create_refrec_df(cls, arcs: list, refrec: list) -> pd.DataFrame:
        """Create a dataframe with items in the proper order from the arcs and reference recipe"""
        # sort the arcs
        arcs = cls._sort_arcs(arcs)
        # initialize a dataframe with the arcs and 0 for value and cost
        refrec_df = pd.DataFrame(arcs, columns=['ingredient', 'target_good']).set_index(['ingredient', 'target_good'])
        refrec_df[['value']] = 0.

        # fill the values
        refrec = pd.DataFrame(refrec, columns=['ingredient', 'target_good', 'value']).set_index(
            ['ingredient', 'target_good'])
        refrec_df.loc[refrec.index.intersection(refrec_df.index), 'value'] = refrec.loc[
            refrec.index.intersection(refrec_df.index), 'value'].values.astype(float)
        refrec_df.reset_index(inplace=True)
        return refrec_df

    @staticmethod
    def _sort_arcs(arcs: list) -> list:
        """Make sure the arcs are in a logical order"""

        def add_items(items: list, sorted_arcs: list) -> list:
            sorted_arcs.extend([item for item in items if item[1] in [item2[0] for item2 in sorted_arcs]])
            return sorted_arcs

        # initialize the list with edges that end in the endpoint
        sorted_arcs = [item for item in arcs if item[1] == FINAL_STAGE_NAME]
        list_size = len([item for item in arcs if item not in sorted_arcs])
        # until all items are in sorted arcs, we add items
        while [item for item in arcs if item not in sorted_arcs]:
            sorted_arcs = add_items([item for item in arcs if item not in sorted_arcs], sorted_arcs)
            if len([item for item in arcs if item not in sorted_arcs]) == list_size:
                break
            list_size = len([item for item in arcs if item not in sorted_arcs])
        # reverse the sorted list and return it
        sorted_arcs.reverse()
        return sorted_arcs

    @staticmethod
    def _format_process_loss(process_loss: list) -> dict:
        """Convert process loss into a dict with a usable structure"""
        process_loss_dict = {}
        if process_loss:
            for loss in process_loss:
                if loss['target_good'] not in process_loss_dict:
                    process_loss_dict[loss['target_good']] = {}
                process_loss_dict[loss['target_good']][loss['quality']] = loss['value']
        return process_loss_dict

    @classmethod
    def _calculate_qualities(cls, profile: pd.DataFrame, refrec: pd.DataFrame, process_loss: list) -> pd.DataFrame:
        """Calculate the qualities for each ingredient and stage in the reference recipe"""
        # convert process loss to a usable format
        process_loss = cls._format_process_loss(process_loss)

        # copy the profile for source ingredients
        cq = profile.copy().select_dtypes('number')
        # drop non-numeric columns
        cq.columns = ["__".join(item) for item in cq.columns]
        cq.fillna(0., inplace=True)

        # add rows for stages
        for stage in list(refrec['ingredient'].unique()) + [FINAL_STAGE_NAME]:
            # if the ingredient is not already in the profile, it is a stage
            if stage not in cq.index:
                stage_ingredients = refrec.loc[refrec['target_good'] == stage]
                stage_total = stage_ingredients['value'].sum()
                if stage_total:
                    cq.loc[stage] = cq.loc[stage_ingredients['ingredient']].multiply(
                        stage_ingredients['value'].values / stage_total, axis=0).sum().values
                else:
                    cq.loc[stage] = 0
                # account for process loss
                if stage in process_loss:
                    for quality, amount in process_loss[stage].items():
                        cq.loc[stage, quality] *= (1 - amount)

        return cq

    def quality(self, quality: str, stage: str = FINAL_STAGE_NAME) -> float:
        """Get the value of the specified quality in the specified stage"""
        if stage in self.cq.index and quality in self.cq.columns:
            # get the total amount of ingredients in the stage
            stage_total = self.refrec.loc[self.refrec['target_good'] == stage, 'value'].sum()
            # the amount is the quality per 100g * total amount in stage as percentage
            response = self.cq.loc[stage, quality] * stage_total
        else:
            response = 0
        return response

    @staticmethod
    def _add_costs(refrec: pd.DataFrame, cost: pd.DataFrame) -> pd.DataFrame:
        """Add the costs to the refrec dataframe"""
        # add costs for source ingredients
        for ing, good, amount in cost[['ingredient', 'target_good', 'cost']].values:
            refrec.loc[(refrec['ingredient'] == ing) & (refrec['target_good'] == good), 'cost'] = refrec.loc[(refrec[
                                                                                                                  'ingredient'] == ing) & (
                                                                                                                     refrec[
                                                                                                                         'target_good'] == good), 'value'] * amount / 100

        # add in costs for stages
        for idx, ing in refrec.loc[refrec['cost'].isna(), 'ingredient'].items():
            if ing in refrec['target_good'].values:
                refrec.loc[idx, 'cost'] = refrec.loc[refrec['target_good'] == ing, 'cost'].sum()

        return refrec

    def scale_values(self, by: float = 100.) -> None:
        """Scale values"""
        self.refrec['value'] /= by

    def value(self, ingredient: str, stage: str = FINAL_STAGE_NAME) -> float:
        """Get the value corresponding to the specified ingredient and stage"""
        filter_idx = (self.refrec['ingredient'] == ingredient) & (self.refrec['target_good'] == stage)
        if filter_idx.sum():
            response = self.refrec.loc[filter_idx, 'value'].values[0]
        else:
            response = 0.

        return response

    def total_value(self, ingredient: str) -> float:
        """Return the total amount of the ingredient over all stages"""
        return self.refrec.loc[self.refrec['ingredient'] == ingredient, 'value'].sum()

    def stage_index(self, stage: str) -> list:
        """Return a list of ingredients present in the specified stage"""
        return list(self.refrec.loc[self.refrec['target_good'] == stage, 'ingredient'].unique())

    def cost_value(self, ingredient: str, stage: str = FINAL_STAGE_NAME) -> float:
        """Get the cost for a specified ingredient and stage"""
        filter_idx = (self.refrec['ingredient'] == ingredient) & (self.refrec['target_good'] == stage)
        if filter_idx.sum():
            response = self.refrec.loc[filter_idx, 'cost'].values[0]
        elif ingredient == FINAL_STAGE_NAME:
            response = self.refrec.loc[self.refrec['target_good'] == FINAL_STAGE_NAME, 'cost'].sum()
        else:
            response = 0.

        return response
