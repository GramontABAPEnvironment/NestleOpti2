import pandas as pd
from constants import FINAL_STAGE_NAME

class VariableTranslator:
    def __init__(self, stage_data: dict = None, bypass: bool = False) -> None:
        """Initialize the object, saving the variable mappings"""
        # if true will NOT rename variables, useful for debugging
        self.bypass = bypass
        self.mapping = {'ingredients': {'evaporation': 'evaporation'}, 'constraints': {}}
        self.reverse_mapping = {}
        if stage_data:
            self.stage_data = stage_data
        else:
            self.stage_data = {}

    def rename_cost_ingredients(self, cost: pd.DataFrame) -> pd.Series:
        """Rename the ingredients column in the cost dataframe"""
        cost['ingredient'] = cost['ingredient'].replace(self.mapping['ingredients'])
        return cost


    def rename_ingredients(self, profile: pd.DataFrame) -> pd.DataFrame:
        """
        Rename the ingredients by changing the index of the dataframe, saving the mapping
        :param profile: dataframe with ingredient information
        :return: return the renamed dataframe
        """
        if not self.bypass:
            self.mapping['ingredients'].update({ingredient: f"ing{i}" for i, ingredient in enumerate(profile.index) if
                                            ingredient != 'evaporation'})

        # create the reverse mapping
        self.reverse_mapping['ingredients'] = {value: key for key, value in self.mapping['ingredients'].items()}
        return profile.rename(index=self.mapping['ingredients'])

    def rename_constraints(self, constraints_df: pd.DataFrame) -> pd.DataFrame:
        """
        Rename the constraints by changing the index of the dataframe, saving the mapping
        :param constraints_df: dataframe with constraints
        :return: renamed dataframe
        """
        if not self.bypass:
            self.mapping['constraints'].update({constraint: f"con{i}" for i, constraint in enumerate(constraints_df.index)})
        self.reverse_mapping['constraints'] = {value: key for key, value in self.mapping['constraints'].items()}
        return constraints_df.rename(index=self.mapping['constraints'])

    def rename_constraints_items(self, constraints_df: pd.DataFrame, type: str = 'ing') -> pd.DataFrame:
        """
        Rename ingredient items in ingredient constraints
        :param constraints: dataframe with constraints
        :param type: type of constraints to rename
        :return: return the renamed dataframe
        """
        for item_col in ['item 1', 'item 2']:
            constraints_df.loc[(constraints_df['type'] == type) & (
                ~constraints_df[item_col].isin(self.stage_data.get('goods', []))), item_col] = constraints_df.loc[
                constraints_df['type'] == type, item_col].replace(self.mapping['ingredients'])

        return constraints_df

    def reverse_rename_constraints(self, constraints_df: pd.DataFrame) -> pd.DataFrame:
        """
        Rename the constraints back to the original names
        """
        return constraints_df.rename(index=self.reverse_mapping['constraints'])

    def rename_loosen_constraints(self, lconstraints: pd.DataFrame) -> list:
        """
        Rename the constraints in lconstraints
        :param lconstraints: dataframe of constraints to loosen
        :return: dataframe with index renamed
        """

        return lconstraints.rename(index=self.mapping['constraints'])

    def reverse_translate(self, var_name: str, key: str = 'ingredients') -> str:
        """
        Get and return the original name for the specified variable
        """
        return self.reverse_mapping[key].get(var_name, var_name)

    def reverse_translate_constraints_list(self, constraint_list: list) -> list:
        """
        Reverse translate the names of a list of dict of constraints
        """
        for constraint in constraint_list:
            constraint['constraint name'] = self.reverse_translate(constraint['constraint name'], 'constraints')
        return constraint_list

    def rename_objectives(self, objectives_list: list) -> list:
        """
        Rename the objectives, as they may include ingredients
        """
        for objective in objectives_list:
            objective['Objective'] = self.mapping['ingredients'].get(objective['Objective'], objective['Objective'])
        return objectives_list

    def reverse_translate_objectives(self, objectives_list: list) -> list:
        """
        Reverse the renaming of the objectives
        """
        for objective in objectives_list:
            objective['Objective'] = self.reverse_mapping['ingredients'].get(objective['Objective'],
                                                                             objective['Objective'])
        return objectives_list

    def rename_arcs(self, arcs_list: list) -> list:
        """Rename all items in the arcs"""
        for arc in arcs_list:
            for i, item in enumerate(arc):
                arc[i] = self.mapping['ingredients'].get(item, item)

        return arcs_list

    def rename_refrec(self, refrec: list) -> list:
        for item in refrec:
            item['ingredient'] = self.mapping['ingredients'].get(item['ingredient'], item['ingredient'])
            if 'target_good' in item:
                item['target_good'] = self.mapping['ingredients'].get(item['target_good'], item['target_good'])
            # if no target good is specified for the refrec we default to the final stage
            else:
                item['target_good'] = FINAL_STAGE_NAME
        return refrec
