# Function call to optimize recipe formulations

## Usage

To use the back-end directly the following `create_and_solve_model` needs to be imported from model_functions.

**Usage example** :

```
from model_functions import create_and_solve_model

results_dict, constraints_loosen_slacks, no_loosen, out_message, instance = create_and_solve_model(
                        ingredients={
                            'profile': profile,
                            'sustainability': sustainability,
                            'otherp': otherp,
                            'AAprofile': AAprofile,
                            'ingtags': ingtags,
                            'refrec': refrec,
                            'cost': cost,
                            'subcomponents': subcomponents,
                        },
                        units=units,
                        constraints={
                            'ing': ing,
                            'profile': profile,
                            'sustainability': sustainability,
                            'otherp': otherp,
                            'class_amount': class_amount,
                        },
                        other_constraints={
                            'classcon': classcon,
                            'scon': scon,
                        },
                        servingc=servingc,
                        objectives=objectives,
                        lconstraints=lconstraints,
                        other_opt=other_opt,
                        auto_loosen = True,
                        process_loss=process_loss,
                        stage_data=stage_data,
                        n_p=10)
```

### Parameters

#### Ingredients

The values in the `ingredients` dict are ingredients and properties of those ingredients. All of the values are lists of
dicts representing dataframes. Each dict must have a key `ingredient` with the name of the ingredient, as well as other
keys with properties of the ingredients.

- profile - contains nutrient amounts per 100g for each ingredient, for an arbitrary list of nutrients
- sustainability - contains sustainability parameters for each ingredient (there is no limitation on the number of
  parameters). It must be consistent with sustainability constraints
- otherp - contains other parameters which can represent any attributes for each ingredient (there is no limitation on
  the number of parameters), as long as the names are consistent between here and the otherp in constraints below,
  containing the constraints on those parameters
- AAprofile - contains amino acid profile of each ingredient, used to calculate PDCAAS. It must contain the following
  properties with all numerical values given in mg-aa/g-total-aa units :
    - ILE
    - LEU
    - LYS
    - MET+CYS
    - PHE+TVR
    - THR
    - TRP
    - VAL
    - HIS
    - digestibility - representing the digestibility of protein in this ingredient, as a percentage from 0 to 100
- ingtags - tags assigning each ingredient to one or more classes, which must be consistent with the `class_amount`
  constraints
- refrec - a reference recipe. It must constain the following properties :
    - value - ingredient amount per 100g
    - target_good - target formulation, must be consistent with stage_data below
- cost - cost per ingredient in a given formulation stage. It must constain the following properties :
    - cost - cost of the ingredient
    - target_good - target formulation, must be consistent with stage_data below
- subcomponents - contains subcomponents for each ingredient (there is no limitation on the number of subcomponents). It
  must be consistent with subcomponents constraints

#### Units

`units` contains a dictionary mapping each column in each of the above mentioned dataframes to a unit. (For ingredients
this should be 'g'.)

#### Constraints

Similary to ingredients, `constraints` is a dict containing list representations of dataframes for each type of
constraint. Each dict must contain the following keys :

- 'constraint name' - the name of the constraint, should be unique, required
- 'item 1' - the column the constraint operates on, required
- 'item 2' - a secondary column the constraint operates on, optional, if not present set to ''
- 'operator' - if the constraint operates on multiple columns this describes how the columns are combined, can be
  either '+', '-', or '/', optional, if not present set to ''
- 'constraint' - the type of constraint, can be either '>=', '<=', or '=', required
- 'value' - the amount of the constraint, should be a number, required
- 'per' - what amount the constraint applies to : '100g', '100ml', '100kcal', or 'serving'. NB ingredient constraints
  MUST be per 100g.
- 'active' - whether the constraint is active or not, should take the values 'yes' or 'no', required
- 'target_good' - target formulation where the constraint is applied, must be consistent with stage_data below. If not
  passed, the constraint is applied to the Final formulation

The keys in this parameter are :

- ing - constraints on ingredients, both item 1 and item 2 keys are correspondingly called ingredient 1 and ingredient
  2, and values must be names of ingredients. All ingredient constraints must be per 100g.
- profile - constraints on nutrients, both item 1 and item 2 keys are correspondingly called nutrient 1 and nutrient 2,
  and must be names of nutrients
- sustainability - constraints on sustainability parameters, both item 1 and item 2 keys are correspondingly called
  sustainability param 1 and sustainability param 2, and values must be names of sustainability parameters
- otherp - constraints on other parameters, both item 1 and item 2 keys are correspondingly called other param 1 and
  other param 2, and values must be names of other parameters
- class_amount - constraints on amounts of class tags, both item 1 and item 2 keys are correspondingly called class name
  1 and class name 2, and values must be names of class tags
- costcon - constraints on cost, item 1 must called 'cost 1' with value 'cost', and item 2 must be called 'cost 2' with
  value ''

#### Other Constraints

`other_constraints` is a dict containing lists representing dataframes of constraints which do not follow the standard
format for constraints described above.

- classcon - constraints on number of ingredients per class tag. Each dict contains the following keys :
    - 'class name' - the name of the class tag
    - 'minimum ingredients' - the minimum number of ingredients from this class to include in the target_good
    - 'maximum ingredients' - the maximum number of ingredients from this class to include in the target_good
    - 'minimum (g/100g)' - the minimum amount of ingredients from this class to include in the target_good
    - 'maximum (g/100g)' - the maximum amount of ingredients from this class to include in the target_good
    - 'target_good' - target formulation where the constraint is applied, must be consistent with stage_data below. If
      not passed, the constraint is applied to the Final formulation. If this key is not passed the constraint is
      applied to the Final recipe by default.
- scon - constraints on scores. Each dict has the following keys :
    - 'score' - the name of the score, currently 'nutriscore_2017', 'nutriscore_2023', 'PDCAAS', 'HSR' and 'Iumami' are
      supported
    - 'min value' - the minimum value for the score
        - Possible values for 'nutriscore_2017': 'A', 'B', 'C', 'D', 'E', 'Not. App.' and ''. The constraint is not set
          if 'Not. App.' or ''
        - Possible values for 'nutriscore_2023': 'A', 'B', 'C', 'D', 'E', 'Not. App.' and ''. The constraint is not set
          if 'Not. App.' or ''
        - Possible values for 'PDCAAS': a number greater than 0 and ''. The constraint is not set if ''
        - Possible values for 'HSR': 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 'Not. App.' and ''. The constraint is not
          set if 'Not. App.' or ''
        - Possible values for 'Iumami': a number greater than 0 and ''. The constraint is not set if ''
    - 'type' - the type of score that should be applied to the recipe (only applicable to nutriscore, PDCAAS and HSR)
        - Possible values for 'nutriscore_2017': 'Solid foods', 'Beverages', 'Not. App.' and ''. The constraint is not
          set if 'Not. App.' or ''
        - Possible values for 'nutriscore_2023': 'Solid foods', 'Animal and vegetable fats', 'Beverages', 'Not. App.'
          and ''. The constraint is not set if 'Not. App.' or ''
        - Possible values for 'PDCAAS': 'FAO 2013 - children > 3y & adults', 'FAO 2013 - children (0.5-3y)' and 'FAO
          2013 - infants (<0.5y)'. The constraint is not set if ''
        - Possible values for 'HSR': 'Non-dairy beverages', 'Foods', 'Fats, oils', 'Dairy beverages', 'Dairy foods', '
          Cheese', 'Not. App.' and ''. The constraint is not set if 'Not. App.' or ''
    - 'digest_type' - the constraint applied for PDCAAS (only applicable to PDCAAS), can be either 'approximate' or '
      actual'
    - 'max value' - the maximum value for Iumami score (only applicable to Iumami). Possible values are a number greater
      than 0 and ''. The constraint is not set if ''. Note that for setting up a Iumami constraint, both min and max
      values must be passed

#### Serving Parameters

`servingc` contains information on serving(portion) sizes, each dict has two keys - 'serving parameter' and 'value'

- 'serving parameter' - describes what the value in the dict describes
    - 'sps_as_sold_g' - the serving(portion) size of the recipe as sold in grams
    - 'sps_as_consummed_g' - the serving(portion) size of the recipe as consummed in grams (water reconstitution)
    - 'dilution factor for nutriscore' - dilution factor used to calculate nutriscore and hsr for drinks that will be
      reconstituted in water. If not provided is calculated as sps_as_consummed_g / sps_as_sold_gloosening
    - 'dp_as_consumed_gml' - density of the final formulation in g/ml. If not provided is 1

#### Objectives

`objectives` contains a list of one or two objectives, with each objective a dict :

- 'Objective' - the name of the objective ('cost' for cost, 'nutritional score 2017' for nutriscore 2017, 'nutritional
  score 2023' for nutriscore 2023, 'HSR points' for hsr, 'pdcaas' for PDCAAS and 'iumami' for Iumami). All source
  ingredients, formulation stages nutrients, sustainability, subcomponents and other parameters are available as
  objectives if passed in the corresponding ingredient properties
- 'Option' - 'minimize' or 'maximize' ('pdcaas' only supports 'maximize')

Note that for all scores a constraint has to be set to have the score available as an objective

#### Constraints to be loosened

`lconstraints` constains a list of dicts of constraints to be loosened :

- 'constraint name' - the name of the constraint to loosen
- 'loosening strength' - the amount of loosening to apply, 'low', 'medium', or 'high'

#### Other Options

`other_opt` containts other options, with a `parameter` and a `value` in each dict. Currently 'evaporation' with a value
of 0 or 1, indicating whether or not water can be evaporated from the Final formulation.

#### Auto-loosening constraints

`auto_loosen` can take values `True` or `False`. If True, all ingerdient constraints are automatically loosened with low
loosening strength in case of an infeasible formulation

#### Process loss

`process_loss` contains list representations of dataframes for the quality loss in a given formulation stage. Each dict
must contain the following keys :

- 'target_good' - target formulation where the loss happens, must be consistent with stage_data below
- 'quality' - quality being lost. The name of the quality should be preceded by the name of the key in which the quality
  appears in the ingredients dict and "__". For example, nutrients should be writted as 'profile__NutrientName' (e.g. '
  profile__protein').
- 'value' - amount lost in percentage fraction (between 0 and 1)

#### Stage data

`stage_data` is a dict containing lists representing the whole formulation tree. The following keys must be provided:

- 'arcs' - list of two-elements-list representing the arcs connecting the formulation stages and ingredients (
  e.g. [['ing0', 'Original'], ['ing9', 'Flour'], ['Flour', 'Final'],['Original', 'Final']])
- 'goods' - list with formulation stage names (e.g. ['Original', 'Flour', 'Final'])

#### Maximum number of formulations

`n_p` is an integer to set the maximum number of formulations to be obtained for multi-objective optimization (default
is 10 if not passed)

### Outputs

The function returns the following items :

- results_dict - a dict containing information about the optimal recipe(s)
- constraints_loosen_slacks - a list of constraints which have been loosened
- no_loosen - a list of constraints which could not be loosened
- out_message - a status message
- instance - the Pyomo instance

#### Results Dict

`results_dict` is a dict containing the following items :

- objective : dict containing the objectives, with for each objective :
    - 'name' - the name of the objective
    - 'unit' - this units for the objective
    - 'reference value' - the value of the objective in the reference recipe
- recipes :  dict with information on each optimal recipe, indexed starting at 1, with the following data :
    - ingredients - dict of ingredients mapping ingredient name to standard data, described below
    - nutrients - dict of nutrients mapping nutrient name to standard data, described below
    - sustainability - dict of sustainability mapping sustainability param name to standard data, described below
    - other parameters - dict of other params mapping other param name to standard data, described below
    - nutriscore data - dict containing optimum and reference values for both the score points and the Nutriscore, as
      well as score breakdown for optimum and reference recipes
    - HSR - dict containing optimum and reference values for both the score points and the Health Star Rating, as well
      as score breakdown for optimum and reference recipes
    - PDCAAS data - dict containing optimum and reference values, as well as amino-acid breakdown
    - Iumami - dict containing optimum and reference values
    - subcomponents - dict containing optimum and reference values
    - optimum_cost - the cost of the current recipe
    - reference cost - the cost of the reference recipe
    - unit_cost - the units for the cost
    - information about each objective - the value of the objective

The standard data for components mentioned above is as follows :

- optimum - optimum value in current recipe
- reference - value in reference recipe
- lbound - lower bound on constraint, if applicable
- ubound - upper bound on constraint, if applicable
- lslack - lower slack amount, if applicable
- uslack - upper slack amount, if applicable

When a formulation stage plays the role of an ingredient the whole recipe structure is nested in the corresponding
ingredient name

## Example input and function call

```python
data = {
   "ingredients":{
      "profile":[
         {
            "ingredient":"ing_0",
            "sugars":50.210468812906036,
            "added sugars":15.372748916311643,
            "protein":31.683075652228876,
            "fiber":34.817664423577874,
            "sodium":55.40488220851012,
            "calcium":36.33248151997614,
            "sfa":16.97234104723218,
            "energy":71.58212637896813,
            "water":65.71431095364363,
            "iron":40.419525109854106
         },
         {
            "ingredient":"ing_1",
            "sugars":28.811211799353245,
            "added sugars":2.5537422654363375,
            "protein":21.908759208243143,
            "fiber":62.450364937274024,
            "sodium":11.830077604642966,
            "calcium":2.644761366130202,
            "sfa":54.03428853601335,
            "energy":65.83726294118047,
            "water":31.09210212449961,
            "iron":20.81532357292929
         },
         {
            "ingredient":"ing_2",
            "sugars":54.573433101704985,
            "added sugars":24.416436351833866,
            "protein":19.95849090156933,
            "fiber":20.831178873029906,
            "sodium":13.170469552592365,
            "calcium":46.49122742392509,
            "sfa":51.70302583059638,
            "energy":51.42954898605695,
            "water":6.333122164396338,
            "iron":12.436069001631486
         },
         {
            "ingredient":"ing_3",
            "sugars":72.35512159302488,
            "added sugars":11.629343322723795,
            "protein":23.487461395236732,
            "fiber":72.84607546204806,
            "sodium":18.561734521147873,
            "calcium":24.497609517089813,
            "sfa":64.2442995300543,
            "energy":15.210114579669726,
            "water":54.91315378071308,
            "iron":33.308052082735166
         },
         {
            "ingredient":"ing_4",
            "sugars":15.52427573762554,
            "added sugars":66.09105032748742,
            "protein":3.8310225144642525,
            "fiber":56.398262245086684,
            "sodium":1.5539819924414278,
            "calcium":66.69618734395542,
            "sfa":52.305139292570566,
            "energy":22.548253896325466,
            "water":67.17557245725777,
            "iron":22.542344549924813
         },
         {
            "ingredient":"ing_5",
            "sugars":23.365355067956827,
            "added sugars":61.536437795281635,
            "protein":69.0992399258628,
            "fiber":6.872920924388937,
            "sodium":10.5313065146483,
            "calcium":37.719591898477866,
            "sfa":34.721155699341374,
            "energy":20.65031426666787,
            "water":34.882151735318715,
            "iron":59.71215713203407
         },
         {
            "ingredient":"ing_6",
            "sugars":53.07376623839064,
            "added sugars":42.84199758504777,
            "protein":30.488903175728115,
            "fiber":20.303325389301378,
            "sodium":29.82703991171748,
            "calcium":30.99512963843113,
            "sfa":17.333752779415953,
            "energy":40.27407333345488,
            "water":32.107476393909245,
            "iron":2.3264269922916414
         },
         {
            "ingredient":"ing_7",
            "sugars":6.710119107474835,
            "added sugars":41.17666927015185,
            "protein":46.38623098583842,
            "fiber":14.670088658241639,
            "sodium":36.92021467120538,
            "calcium":4.532836778318982,
            "sfa":6.758455003147268,
            "energy":19.564393569462098,
            "water":14.866151771378583,
            "iron":59.920029419381315
         },
         {
            "ingredient":"ing_8",
            "sugars":67.59703215332894,
            "added sugars":36.928551067679734,
            "protein":8.302159219539151,
            "fiber":55.86249436795555,
            "sodium":34.81294311462976,
            "calcium":72.17830219248172,
            "sfa":10.987429339764502,
            "energy":61.681210933235846,
            "water":56.61720603393184,
            "iron":69.86452365173045
         },
         {
            "ingredient":"ing_9",
            "sugars":16.417044103109234,
            "added sugars":21.68969768017482,
            "protein":25.496835637093675,
            "fiber":14.329092644518571,
            "sodium":34.80078818568087,
            "calcium":46.65770345461839,
            "sfa":39.89272328550022,
            "energy":55.42608300879656,
            "water":10.662134216781736,
            "iron":6.311278269337809
         },
         {
            "ingredient":"ing_10",
            "sugars":69.12305777127004,
            "added sugars":34.574026489256724,
            "protein":8.880710614801915,
            "fiber":47.87664711682139,
            "sodium":19.70702222940424,
            "calcium":55.22033948119084,
            "sfa":26.552984406359805,
            "energy":64.67083664753623,
            "water":69.62226627513552,
            "iron":44.92952528146909
         },
         {
            "ingredient":"ing_11",
            "sugars":32.0951051300393,
            "added sugars":35.044442118289695,
            "protein":3.5719927224776264,
            "fiber":73.91386593348115,
            "sodium":33.16524664319333,
            "calcium":62.87738937706474,
            "sfa":69.16089804832397,
            "energy":48.64258560129898,
            "water":63.97415309235984,
            "iron":54.860648150843865
         }
      ],
      "sustainability":[
         {
            "ingredient":"ing_0",
            "GHGe":1.51
         },
         {
            "ingredient":"ing_1",
            "GHGe":12.0
         },
         {
            "ingredient":"ing_2",
            "GHGe":0.0006
         },
         {
            "ingredient":"ing_3",
            "GHGe":2.1
         },
         {
            "ingredient":"ing_4",
            "GHGe":4.41
         },
         {
            "ingredient":"ing_5",
            "GHGe":2.1
         },
         {
            "ingredient":"ing_6",
            "GHGe":2.1
         },
         {
            "ingredient":"ing_7",
            "GHGe":2.18
         },
         {
            "ingredient":"ing_8",
            "GHGe":18.12
         },
         {
            "ingredient":"ing_9",
            "GHGe":1.25
         },
         {
            "ingredient":"ing_10",
            "GHGe":1.03
         },
         {
            "ingredient":"ing_11",
            "GHGe":0.0
         }
      ],
      "otherp":[
         {
            "ingredient":"ing_0",
            "property_1":15,
            "property_2":0
         },
         {
            "ingredient":"ing_1",
            "property_1":14,
            "property_2":12
         },
         {
            "ingredient":"ing_2",
            "property_1":2,
            "property_2":19
         },
         {
            "ingredient":"ing_3",
            "property_1":7,
            "property_2":13
         },
         {
            "ingredient":"ing_4",
            "property_1":19,
            "property_2":2
         },
         {
            "ingredient":"ing_5",
            "property_1":0,
            "property_2":18
         },
         {
            "ingredient":"ing_6",
            "property_1":12,
            "property_2":11
         },
         {
            "ingredient":"ing_7",
            "property_1":19,
            "property_2":5
         },
         {
            "ingredient":"ing_8",
            "property_1":1,
            "property_2":0
         },
         {
            "ingredient":"ing_9",
            "property_1":19,
            "property_2":16
         },
         {
            "ingredient":"ing_10",
            "property_1":14,
            "property_2":8
         },
         {
            "ingredient":"ing_11",
            "property_1":4,
            "property_2":20
         }
      ],
      "AAprofile":[
         {
            "ingredient":"ing_0",
            "ILE":57.3,
            "LEU":94.2,
            "LYS":82.2,
            "MET+CYS":26.8,
            "PHE+TYR":102.5,
            "THR":43.5,
            "TRP":15.1,
            "VAL":63.0,
            "HIS":26.2,
            "digestibility":95
         },
         {
            "ingredient":"ing_1",
            "ILE":0.0,
            "LEU":0.0,
            "LYS":0.0,
            "MET+CYS":0.0,
            "PHE+TYR":0.0,
            "THR":0.0,
            "TRP":0.0,
            "VAL":0.0,
            "HIS":0.0,
            "digestibility":0
         },
         {
            "ingredient":"ing_2",
            "ILE":0.0,
            "LEU":0.0,
            "LYS":0.0,
            "MET+CYS":0.0,
            "PHE+TYR":0.0,
            "THR":0.0,
            "TRP":0.0,
            "VAL":0.0,
            "HIS":0.0,
            "digestibility":0
         },
         {
            "ingredient":"ing_3",
            "ILE":0.0,
            "LEU":0.0,
            "LYS":0.0,
            "MET+CYS":0.0,
            "PHE+TYR":0.0,
            "THR":0.0,
            "TRP":0.0,
            "VAL":0.0,
            "HIS":0.0,
            "digestibility":0
         },
         {
            "ingredient":"ing_4",
            "ILE":0.0,
            "LEU":0.0,
            "LYS":0.0,
            "MET+CYS":0.0,
            "PHE+TYR":0.0,
            "THR":0.0,
            "TRP":0.0,
            "VAL":0.0,
            "HIS":0.0,
            "digestibility":0
         },
         {
            "ingredient":"ing_5",
            "ILE":0.0,
            "LEU":0.0,
            "LYS":0.0,
            "MET+CYS":0.0,
            "PHE+TYR":0.0,
            "THR":0.0,
            "TRP":0.0,
            "VAL":0.0,
            "HIS":0.0,
            "digestibility":0
         },
         {
            "ingredient":"ing_6",
            "ILE":0.0,
            "LEU":0.0,
            "LYS":0.0,
            "MET+CYS":0.0,
            "PHE+TYR":0.0,
            "THR":0.0,
            "TRP":0.0,
            "VAL":0.0,
            "HIS":0.0,
            "digestibility":0
         },
         {
            "ingredient":"ing_7",
            "ILE":0.0,
            "LEU":0.0,
            "LYS":0.0,
            "MET+CYS":0.0,
            "PHE+TYR":0.0,
            "THR":0.0,
            "TRP":0.0,
            "VAL":0.0,
            "HIS":0.0,
            "digestibility":0
         },
         {
            "ingredient":"ing_8",
            "ILE":0.0,
            "LEU":0.0,
            "LYS":0.0,
            "MET+CYS":0.0,
            "PHE+TYR":0.0,
            "THR":0.0,
            "TRP":0.0,
            "VAL":0.0,
            "HIS":0.0,
            "digestibility":0
         },
         {
            "ingredient":"ing_9",
            "ILE":35.8,
            "LEU":122.8,
            "LYS":28.2,
            "MET+CYS":39.0,
            "PHE+TYR":89.9,
            "THR":37.7,
            "TRP":7.1,
            "VAL":50.7,
            "HIS":30.5,
            "digestibility":87
         },
         {
            "ingredient":"ing_10",
            "ILE":41.0,
            "LEU":82.0,
            "LYS":34.8,
            "MET+CYS":42.2,
            "PHE+TYR":106.1,
            "THR":35.3,
            "TRP":12.1,
            "VAL":58.5,
            "HIS":25.0,
            "digestibility":88
         },
         {
            "ingredient":"ing_11",
            "ILE":37.1,
            "LEU":69.1,
            "LYS":19.3,
            "MET+CYS":40.0,
            "PHE+TYR":76.7,
            "THR":26.7,
            "TRP":11.6,
            "VAL":41.9,
            "HIS":21.2,
            "digestibility":96
         }
      ],
      "ingtags":[
         {
            "ingredient":"ing_0",
            "class 1":"class_1",
            "class 2":"",
            "class 3":"class_2"
         },
         {
            "ingredient":"ing_1",
            "class 1":"class_1",
            "class 2":"",
            "class 3":"class_2"
         },
         {
            "ingredient":"ing_2",
            "class 1":"class_1",
            "class 2":"",
            "class 3":"class_2"
         },
         {
            "ingredient":"ing_3",
            "class 1":"class_1",
            "class 2":"",
            "class 3":"class_2"
         },
         {
            "ingredient":"ing_4",
            "class 1":"class_1",
            "class 2":"",
            "class 3":"food2"
         },
         {
            "ingredient":"ing_5",
            "class 1":"class_1",
            "class 2":"",
            "class 3":""
         },
         {
            "ingredient":"ing_6",
            "class 1":"class_1",
            "class 2":"",
            "class 3":""
         },
         {
            "ingredient":"ing_7",
            "class 1":"class_1",
            "class 2":"",
            "class 3":""
         },
         {
            "ingredient":"ing_8",
            "class 1":"class_1",
            "class 2":"",
            "class 3":""
         },
         {
            "ingredient":"ing_9",
            "class 1":"",
            "class 2":"class_3",
            "class 3":""
         },
         {
            "ingredient":"ing_10",
            "class 1":"",
            "class 2":"class_3",
            "class 3":""
         },
         {
            "ingredient":"ing_11",
            "class 1":"",
            "class 2":"class_3",
            "class 3":""
         }
      ],
      "refrec":[
         {
            "ingredient":"ing_0",
            "value":52.464,
            "target_good": "Stage_2"
         },
         {
            "ingredient":"ing_1",
            "value":20.354,
            "target_good": "Stage_2"
         },
         {
            "ingredient":"ing_2",
            "value":3.177,
            "target_good": "Stage_2"
         },
         {
            "ingredient":"ing_3",
            "value":0.22999999999999998,
            "target_good": "Stage_2"
         },
         {
            "ingredient":"ing_4",
            "value":0.297,
            "target_good": "Stage_2"
         },
         {
            "ingredient":"ing_5",
            "value":0.15489,
            "target_good": "Stage_2"
         },
         {
            "ingredient":"ing_6",
            "value":1.7999999999999998,
            "target_good": "Stage_2"
         },
         {
            "ingredient":"ing_7",
            "value":11.790000000000001,
            "target_good": "Stage_2"
         },
         {
            "ingredient":"ing_8",
            "value":9.700000000000001,
            "target_good": "Stage_2"
         },
         {
            "ingredient":"ing_9",
            "value":0.0,
            "target_good": "Stage_1"
         },
         {
            "ingredient":"ing_10",
            "value":0.0,
            "target_good": "Stage_1"
         },
         {
            "ingredient":"ing_11",
            "value":0.0,
            "target_good": "Stage_1"
         },
         {
            "ingredient":"Stage_1",
            "value":100.0,
            "target_good": "Final"
         },
         {
            "ingredient":"Stage_2",
            "value":100.0,
            "target_good": "Final"
         }
      ],
      "cost":[
         {
            "ingredient":"ing_0",
            "cost":16.57,
            "target_good":"Stage_2"
         },
         {
            "ingredient":"ing_1",
            "cost":25.99,
            "target_good":"Stage_2"
         },
         {
            "ingredient":"ing_2",
            "cost":0.0,
            "target_good":"Stage_2"
         },
         {
            "ingredient":"ing_3",
            "cost":66.33,
            "target_good":"Stage_2"
         },
         {
            "ingredient":"ing_4",
            "cost":21.88,
            "target_good":"Stage_2"
         },
         {
            "ingredient":"ing_5",
            "cost":41.89,
            "target_good":"Stage_2"
         },
         {
            "ingredient":"ing_6",
            "cost":2.13,
            "target_good":"Stage_2"
         },
         {
            "ingredient":"ing_7",
            "cost":9.34,
            "target_good":"Stage_2"
         },
         {
            "ingredient":"ing_8",
            "cost":5.24,
            "target_good":"Stage_2"
         },
         {
            "ingredient":"ing_9",
            "cost":1.5,
            "target_good":"Stage_1"
         },
         {
            "ingredient":"ing_10",
            "cost":5.17,
            "target_good":"Stage_1"
         },
         {
            "ingredient":"ing_11",
            "cost":3.63,
            "target_good":"Stage_1"
         }
      ]
   },
   "units":{
      "sugars":"g/100g",
      "added sugars":"g/100g",
      "protein":"g/100g",
      "fiber":"g/100g",
      "sodium":"mg/100g",
      "calcium":"mg/100g",
      "sfa":"g/100g",
      "energy":"kcal/100g",
      "water":"g/100g",
      "iron":"mg/100g",
      "GHGe":"kg/kg",
      "cost":"USD/kg",
      "evaporation":"g",
      "nutritional score":"",
      "PDCAAS":"",
      "ing_0":"g",
      "ing_1":"g",
      "ing_2":"g",
      "ing_3":"g",
      "ing_4":"g",
      "ing_5":"g",
      "ing_6":"g",
      "ing_7":"g",
      "ing_8":"g",
      "ing_9":"g",
      "ing_10":"g",
      "ing_11":"g"
   },
   "constraints":{
      "ing":[
         {
            "constraint name":"constraint_0",
            "ingredient 1":"ing_0",
            "operator":"",
            "ingredient 2":"",
            "constraint":">=",
            "value":35.0,
            "active":"yes",
            "target_good":"Stage_2"
         },
         {
            "constraint name":"constraint_1",
            "ingredient 1":"ing_0",
            "operator":"",
            "ingredient 2":"",
            "constraint":"<=",
            "value":50.0,
            "active":"yes",
            "target_good":"Stage_2"
         },
         {
            "constraint name":"constraint_2",
            "ingredient 1":"ing_1",
            "operator":"",
            "ingredient 2":"",
            "constraint":">=",
            "value":15.0,
            "active":"yes",
            "target_good":"Stage_2"
         },
         {
            "constraint name":"constraint_3",
            "ingredient 1":"ing_1",
            "operator":"",
            "ingredient 2":"",
            "constraint":"<=",
            "value":20.0,
            "active":"yes",
            "target_good":"Stage_2"
         },
         {
            "constraint name":"constraint_4",
            "ingredient 1":"ing_2",
            "operator":"",
            "ingredient 2":"",
            "constraint":">=",
            "value":2.0,
            "active":"yes",
            "target_good":"Stage_2"
         },
         {
            "constraint name":"constraint_5",
            "ingredient 1":"ing_2",
            "operator":"",
            "ingredient 2":"",
            "constraint":"<=",
            "value":3.5,
            "active":"yes",
            "target_good":"Stage_2"
         },
         {
            "constraint name":"constraint_6",
            "ingredient 1":"ing_3",
            "operator":"",
            "ingredient 2":"",
            "constraint":">=",
            "value":0.23,
            "active":"yes",
            "target_good":"Stage_2"
         },
         {
            "constraint name":"constraint_7",
            "ingredient 1":"ing_3",
            "operator":"",
            "ingredient 2":"",
            "constraint":"<=",
            "value":0.23,
            "active":"yes",
            "target_good":"Stage_2"
         },
         {
            "constraint name":"constraint_8",
            "ingredient 1":"ing_4",
            "operator":"",
            "ingredient 2":"",
            "constraint":">=",
            "value":0.297,
            "active":"yes",
            "target_good":"Stage_2"
         },
         {
            "constraint name":"constraint_9",
            "ingredient 1":"ing_4",
            "operator":"",
            "ingredient 2":"",
            "constraint":"<=",
            "value":0.297,
            "active":"yes",
            "target_good":"Stage_2"
         },
         {
            "constraint name":"constraint_10",
            "ingredient 1":"ing_5",
            "operator":"",
            "ingredient 2":"",
            "constraint":">=",
            "value":0.155,
            "active":"yes",
            "target_good":"Stage_2"
         },
         {
            "constraint name":"constraint_11",
            "ingredient 1":"ing_5",
            "operator":"",
            "ingredient 2":"",
            "constraint":"<=",
            "value":0.155,
            "active":"yes",
            "target_good":"Stage_2"
         },
         {
            "constraint name":"constraint_12",
            "ingredient 1":"ing_6",
            "operator":"",
            "ingredient 2":"",
            "constraint":">=",
            "value":1.0,
            "active":"yes",
            "target_good":"Stage_2"
         },
         {
            "constraint name":"constraint_13",
            "ingredient 1":"ing_6",
            "operator":"",
            "ingredient 2":"",
            "constraint":"<=",
            "value":2.0,
            "active":"yes",
            "target_good":"Stage_2"
         },
         {
            "constraint name":"constraint_14",
            "ingredient 1":"ing_7",
            "operator":"",
            "ingredient 2":"",
            "constraint":">=",
            "value":10.0,
            "active":"yes",
            "target_good":"Stage_2"
         },
         {
            "constraint name":"constraint_15",
            "ingredient 1":"ing_7",
            "operator":"",
            "ingredient 2":"",
            "constraint":"<=",
            "value":15.0,
            "active":"yes",
            "target_good":"Stage_2"
         },
         {
            "constraint name":"constraint_16",
            "ingredient 1":"ing_8",
            "operator":"",
            "ingredient 2":"",
            "constraint":"<=",
            "value":100.0,
            "active":"yes",
            "target_good":"Stage_2"
         },
         {
            "constraint name":"constraint_17",
            "ingredient 1":"ing_9",
            "operator":"",
            "ingredient 2":"",
            "constraint":"<=",
            "value":100,
            "active":"yes",
            "target_good":"Stage_1"
         },
         {
            "constraint name":"constraint_18",
            "ingredient 1":"ing_10",
            "operator":"",
            "ingredient 2":"",
            "constraint":"<=",
            "value":100,
            "active":"yes",
            "target_good":"Stage_1"
         },
         {
            "constraint name":"constraint_19",
            "ingredient 1":"ing_11",
            "operator":"",
            "ingredient 2":"",
            "constraint":"<=",
            "value":100,
            "active":"yes",
            "target_good":"Stage_1"
         }
      ],
      "profile":[
         {
            "constraint name":"sugars lower",
            "nutrient 1":"sugars",
            "operator":"",
            "nutrient 2":"",
            "constraint":">=",
            "value":36.0,
            "per":"100g",
            "active":"yes",
            "target_good":"Final"
         },
         {
            "constraint name":"sugars upper",
            "nutrient 1":"sugars",
            "operator":"",
            "nutrient 2":"",
            "constraint":"<=",
            "value":40.0,
            "per":"100g",
            "active":"yes",
            "target_good":"Final"
         },
         {
            "constraint name":"added sugars upper",
            "nutrient 1":"added sugars",
            "operator":"",
            "nutrient 2":"",
            "constraint":"<=",
            "value":10.6,
            "per":"serving",
            "active":"yes",
            "target_good":"Final"
         },
         {
            "constraint name":"protein lower 1",
            "nutrient 1":"protein",
            "operator":"",
            "nutrient 2":"",
            "constraint":">=",
            "value":2.2,
            "per":"100ml",
            "active":"yes",
            "target_good":"Final"
         },
         {
            "constraint name":"protein lower 2",
            "nutrient 1":"protein",
            "operator":"",
            "nutrient 2":"",
            "constraint":">=",
            "value":18.0,
            "per":"100g",
            "active":"yes",
            "target_good":"Final"
         },
         {
            "constraint name":"fiber lower",
            "nutrient 1":"fiber",
            "operator":"",
            "nutrient 2":"",
            "constraint":">=",
            "value":10.0,
            "per":"100g",
            "active":"yes",
            "target_good":"Final"
         },
         {
            "constraint name":"fiber upper",
            "nutrient 1":"fiber",
            "operator":"",
            "nutrient 2":"",
            "constraint":"<=",
            "value":12.0,
            "per":"100g",
            "active":"yes",
            "target_good":"Final"
         },
         {
            "constraint name":"sodium upper",
            "nutrient 1":"sodium",
            "operator":"",
            "nutrient 2":"",
            "constraint":"<=",
            "value":140.0,
            "per":"serving",
            "active":"yes",
            "target_good":"Final"
         },
         {
            "constraint name":"calcium lower",
            "nutrient 1":"calcium",
            "operator":"",
            "nutrient 2":"",
            "constraint":">=",
            "value":105.0,
            "per":"100kcal",
            "active":"yes",
            "target_good":"Final"
         },
         {
            "constraint name":"sfa upper",
            "nutrient 1":"sfa",
            "operator":"",
            "nutrient 2":"",
            "constraint":"<=",
            "value":2.5,
            "per":"100ml",
            "active":"yes",
            "target_good":"Final"
         },
         {
            "constraint name":"energy upper",
            "nutrient 1":"energy",
            "operator":"",
            "nutrient 2":"",
            "constraint":"<=",
            "value":170.0,
            "per":"serving",
            "active":"yes",
            "target_good":"Final"
         },
         {
            "constraint name":"water nut upper",
            "nutrient 1":"water",
            "operator":"",
            "nutrient 2":"",
            "constraint":"<=",
            "value":5.0,
            "per":"100g",
            "active":"yes",
            "target_good":"Final"
         }
      ],
      "sustainability":[
         {
            "constraint name":"sus_constraint1",
            "sustainability param 1":"GHGe",
            "operator":"",
            "sustainability param 2":"",
            "constraint":"<=",
            "value":4.0,
            "per":"100g",
            "active":"yes",
            "target_good":"Final"
         }
      ],
      "otherp":[
         {
            "constraint name":"property 1 upper",
            "other param 1":"property_1",
            "value":2.5,
            "constraint":"<=",
            "per":"100g",
            "active":"yes",
            "other param 2":"",
            "operator":""
         },
         {
            "constraint name":"property 2 lower",
            "other param 1":"property_2",
            "value":9,
            "constraint":">=",
            "per":"100g",
            "active":"yes",
            "other param 2":"",
            "operator":""
         }
      ],
      "class_amount":[
         {
            "constraint name":"class_2 + class_3 lower",
            "class name 1":"class_2",
            "constraint":">=",
            "per":"100g",
            "active":"yes",
            "value":20.0,
            "operator":"+",
            "class name 2":"class_3",
            "target_good":"Final"
         }
      ]
   },
   "other_constraints":{
      "classcon":[
         {
            "class name":"class_1",
            "minimum ingredients":0.0,
            "maximum ingredients":8.0,
         },
         {
            "class name":"class_3",
            "minimum ingredients":0.0,
            "maximum ingredients":3.0,
         },
         {
            "class name":"food2",
            "minimum ingredients":0.0,
            "maximum ingredients":1.0,
         },
         {
            "class name":"class_2",
            "minimum ingredients":0.0,
            "maximum ingredients":4.0,
         }
      ],
      "scon":[
         {
            "score":"nutriscore_2023",
            "min value":"E",
            "type":"Beverages"
         },
         {
            "score":"PDCAAS",
            "min value":0.1,
            "type":"FAO 2013 - children > 3y & adults",
            "digest_type": "actual"
         },
         {
            "score":"HSR",
            "min value":0.5,
            "type":"Foods"
         },
         {
            "score":"Iumami",
            "min value":"",
            "max value":""
         }
      ],      
   },
   "servingc":[
      {
         "serving parameter":"sps_as_sold_g",
         "value":25.0
      },
      {
         "serving parameter":"sps_as_consummed_g",
         "value":200.0
      },
      {
         "serving parameter":"dilution factor for nutriscore",
         "value":""
      },
      {
         "serving parameter":"dp_as_consumed_gml",
         "value":1
      }
   ],
   "objectives":[
      {
         "Objective":"cost",
         "Option":"minimize"
      }
   ],
   "lconstraints":[
      {
         "constraint name":"constraint_1",
         "loosening strength":"medium"
      },
      {
         "constraint name":"constraint_2",
         "loosening strength":"low"
      },
      {
         "constraint name":"property 1 upper",
         "loosening strength":"high"
      },
      {
         "constraint name":"property 2 lower",
         "loosening strength":"high"
      },
      {
         "constraint name":"class_2 + class_3 lower",
         "loosening strength":"high"
      },
      {
         "constraint name":"sugars lower",
         "loosening strength":"high"
      },
      {
         "constraint name":"sugars upper",
         "loosening strength":"high"
      },
      {
         "constraint name":"added sugars upper",
         "loosening strength":"high"
      },
      {
         "constraint name":"protein lower 1",
         "loosening strength":"high"
      },
      {
         "constraint name":"protein lower 2",
         "loosening strength":"high"
      },
      {
         "constraint name":"fiber lower",
         "loosening strength":"high"
      },
      {
         "constraint name":"fiber upper",
         "loosening strength":"high"
      },
      {
         "constraint name":"sodium upper",
         "loosening strength":"high"
      },
      {
         "constraint name":"calcium lower",
         "loosening strength":"high"
      },
      {
         "constraint name":"sfa upper",
         "loosening strength":"high"
      },
      {
         "constraint name":"energy upper",
         "loosening strength":"high"
      },
      {
         "constraint name":"water nut upper",
         "loosening strength":"high"
      },
      {
         "constraint name":"sus_constraint1",
         "loosening strength":"high"
      },            
   ],
   "other_opt":[
      {
         "parameter":"evaporation",
         "value":1
      }
   ],
   "stage_data": {
       "arcs":[
           ["ing_0", "Stage_2"], 
           ["ing_1", "Stage_2"],
           ["ing_2", "Stage_2"], 
           ["ing_3", "Stage_2"], 
           ["ing_4", "Stage_2"], 
           ["ing_5", "Stage_2"], 
           ["ing_6", "Stage_2"], 
           ["ing_7", "Stage_2"], 
           ["ing_8", "Stage_2"], 
           ["ing_9", "Stage_1"], 
           ["ing_10", "Stage_1"], 
           ["ing_11", "Stage_1"], 
           ["Stage_1", "Final"],
           ["Stage_2", "Final"]
        ]
    }
}

results_dict, constraints_loosen_slacks, no_loosen, out_message, instance = create_and_solve_model(**data,
                                                                                                   process_loss = [{
                                                                                                                     'target_good': 'Final',
                                                                                                                     'quality': 'profile__sugars',
                                                                                                                     'value': 0.10}],
                                                                                                    auto_loosen = True,
                                                                                                    n_p=10
                                                                                                                 )
 
```

## Example corresponding output ```results_dict```

```python

{'objective': {1: {'name': 'cost',
   'option': 'minimize',
   'unit': 'USD/kg',
   'reference value': 15.913521421}},
 'recipes': {1: {'ingredients': {'Stage_2': {'recipe': {'ingredients': {'ing_0': {'optimum': 0.0,
        'reference': 52.464,
        'optimum_cost': 0.0,
        'reference_cost': 8.6932848,
        'lbound': 35.0,
        'ubound': 50.0,
        'lslack': inf,
        'uslack': 0.0},
       'ing_1': {'optimum': 0.0,
        'reference': 20.354,
        'optimum_cost': 0.0,
        'reference_cost': 5.2900046,
        'lbound': 15.0,
        'ubound': 20.0,
        'lslack': inf,
        'uslack': 0.0},
       'ing_2': {'optimum': 0.0,
        'reference': 3.177,
        'optimum_cost': 0.0,
        'reference_cost': 0.0,
        'lbound': 2.0,
        'ubound': 3.5000000000000004,
        'lslack': inf,
        'uslack': 0.0},
       'ing_3': {'optimum': 0.0,
        'reference': 0.22999999999999998,
        'optimum_cost': 0.0,
        'reference_cost': 0.152559,
        'lbound': 0.22999999999999998,
        'ubound': 0.22999999999999998,
        'lslack': inf,
        'uslack': 0.0},
       'ing_4': {'optimum': 0.0,
        'reference': 0.297,
        'optimum_cost': 0.0,
        'reference_cost': 0.06498359999999999,
        'lbound': 0.297,
        'ubound': 0.297,
        'lslack': inf,
        'uslack': 0.0},
       'ing_5': {'optimum': 0.0,
        'reference': 0.15489,
        'optimum_cost': 0.0,
        'reference_cost': 0.064883421,
        'lbound': 0.155,
        'ubound': 0.155,
        'lslack': inf,
        'uslack': 0.0},
       'ing_6': {'optimum': 0.0,
        'reference': 1.7999999999999998,
        'optimum_cost': 0.0,
        'reference_cost': 0.03834,
        'lbound': 1.0,
        'ubound': 2.0,
        'lslack': inf,
        'uslack': 0.0},
       'ing_7': {'optimum': 0.0,
        'reference': 11.790000000000001,
        'optimum_cost': 0.0,
        'reference_cost': 1.101186,
        'lbound': 10.0,
        'ubound': 15.0,
        'lslack': inf,
        'uslack': 0.0},
       'ing_8': {'optimum': 0.0,
        'reference': 9.700000000000001,
        'optimum_cost': 0.0,
        'reference_cost': 0.5082800000000001,
        'lbound': nan,
        'ubound': 100.0,
        'lslack': nan,
        'uslack': 0.0}},
      'nutrients': {'sugars': {'optimum': 0.0,
        'reference': 42.492529808289234,
        'lbound': 36.0,
        'ubound': 40.0,
        'lslack': -21.224660307201688,
        'uslack': 25.224660307201688},
       'added sugars': {'optimum': 0.0,
        'reference': 18.886964289721124,
        'lbound': nan,
        'ubound': 42.4,
        'lslack': nan,
        'uslack': 20.71030231982518},
       'protein': {'optimum': 0.0,
        'reference': 28.711072360860953,
        'lbound': 18.0,
        'ubound': nan,
        'lslack': 7.496835637093675,
        'uslack': nan},
       'fiber': {'optimum': 0.0,
        'reference': 39.49911283847102,
        'lbound': 10.0,
        'ubound': 12.0,
        'lslack': 4.329092644518571,
        'uslack': -2.329092644518571},
       'sodium': {'optimum': 0.0,
        'reference': 40.22419198204948,
        'lbound': nan,
        'ubound': 560.0,
        'lslack': nan,
        'uslack': 525.1992118143191},
       'calcium': {'optimum': 0.0,
        'reference': 29.483299284879227,
        'lbound': 58.197387159236385,
        'ubound': nan,
        'lslack': inf,
        'uslack': nan},
       'sfa': {'optimum': 0.0,
        'reference': 24.07661101781657,
        'lbound': nan,
        'ubound': 20.0,
        'lslack': nan,
        'uslack': -19.892723285500217},
       'energy': {'optimum': 0.0,
        'reference': 61.73786968553536,
        'lbound': nan,
        'ubound': 680.0,
        'lslack': nan,
        'uslack': 624.5739169912034},
       'water': {'optimum': 0.0,
        'reference': 49.20840937924693,
        'lbound': nan,
        'ubound': 5.0,
        'lslack': nan,
        'uslack': -5.662134216781736},
       'iron': {'optimum': 0.0,
        'reference': 39.95689791775926,
        'lbound': nan,
        'ubound': nan,
        'lslack': nan,
        'uslack': nan}},
      'sustainability': {'GHGe': {'optimum': 0.0,
        'reference': 5.308347852000001,
        'lbound': nan,
        'ubound': 4.0,
        'lslack': nan,
        'uslack': 2.75}},
      'other parameters': {'property_1': {'optimum': 0.0,
        'reference': 13.40833,
        'lbound': nan,
        'ubound': 2.5,
        'lslack': nan,
        'uslack': -16.5},
       'property_2': {'optimum': 0.0,
        'reference': 3.8973302000000003,
        'lbound': 9.0,
        'ubound': nan,
        'lslack': 7.0,
        'uslack': nan}},
      'nutriscore data': {'score': {'optimum': -2.0, 'reference': -2.0},
       'NutriScore': {'optimum': 'B', 'reference': 'B'},
       'score_break_down': {'optimum': {'sugars': {'value': 1.8469174615997888,
          'score': 1.0},
         'protein': {'value': 3.1871044546367093, 'score': 7.0},
         'fiber': {'value': 1.7911365805648214, 'score': 0.0},
         'salt': {'value': 0.010875246308025274, 'score': 0.0},
         'fvpno_eff': {'value': 0.0, 'score': 0.0},
         'sfa': {'value': 4.986590410687527, 'score': 4.0},
         'energy': {'value': 6.92826037609957, 'score': 0.0},
         'nn_sweeteners': {'value': 0.0, 'score': 0.0}},
        'reference': {'sugars': {'value': 4.7819929212887775, 'score': 3.0},
         'protein': {'value': 3.5900727181846097, 'score': 7.0},
         'fiber': {'value': 4.939024415792947, 'score': 2.0},
         'salt': {'value': 0.012574223319731626, 'score': 0.0},
         'fvpno_eff': {'value': 0, 'score': 0.0},
         'sfa': {'value': 3.010573178006309, 'score': 3.0},
         'energy': {'value': 7.719789733072539, 'score': 1.0},
         'nn_sweeteners': {'value': 0, 'score': 0.0}}},
       'version': 'nutriscore_2023'},
      'HSR': {'points': {'optimum': 2.0, 'reference': -4.0},
       'score': {'optimum': 3.5, 'reference': 4},
       'score_break_down': {'optimum': {'sugars': {'value': 1.8469174615997888,
          'score': 0.0},
         'protein': {'value': 3.1871044546367093, 'score': 1.0},
         'fiber': {'value': 1.7911365805648214, 'score': 1.0},
         'sodium': {'value': 4.350098523210109, 'score': 0.0},
         'sfa': {'value': 4.986590410687527, 'score': 4.0},
         'energy': {'value': 6.92826037609957, 'score': 0.0},
         'fv_c': {'value': 0.0, 'score': 0.0},
         'fvnl_nc': {'value': 0.0, 'score': 0.0}},
        'reference': {'sugars': {'value': 4.7819929212887775, 'score': 0.0},
         'protein': {'value': 3.5900727181846097, 'score': 2.0},
         'fiber': {'value': 4.939024415792947, 'score': 5.0},
         'sodium': {'value': 5.02968932789265, 'score': 0.0},
         'sfa': {'value': 3.010573178006309, 'score': 3.0},
         'energy': {'value': 7.719789733072539, 'score': 0.0},
         'fv_c': {'value': 0, 'score': 0.0},
         'fvnl_nc': {'value': 0, 'score': 0.0}}}},
      'PDCAAS data': {'reference': 1.1069565217391304,
       'optimum': 0.511125,
       'AA_breakdown': {'optimum': {'ILE': {'ing_0': 0.0,
          'ing_1': 0.0,
          'ing_2': 0.0,
          'ing_3': 0.0,
          'ing_4': 0.0,
          'ing_5': 0.0,
          'ing_6': 0.0,
          'ing_7': 0.0,
          'ing_8': 0.0,
          'ing_9': 35.8,
          'ing_10': 0.0,
          'ing_11': 0.0,
          'evaporation': 0.0,
          'pattern': 30},
         'LEU': {'ing_0': 0.0,
          'ing_1': 0.0,
          'ing_2': 0.0,
          'ing_3': 0.0,
          'ing_4': 0.0,
          'ing_5': 0.0,
          'ing_6': 0.0,
          'ing_7': 0.0,
          'ing_8': 0.0,
          'ing_9': 122.8,
          'ing_10': 0.0,
          'ing_11': 0.0,
          'evaporation': 0.0,
          'pattern': 61},
         'LYS': {'ing_0': 0.0,
          'ing_1': 0.0,
          'ing_2': 0.0,
          'ing_3': 0.0,
          'ing_4': 0.0,
          'ing_5': 0.0,
          'ing_6': 0.0,
          'ing_7': 0.0,
          'ing_8': 0.0,
          'ing_9': 28.2,
          'ing_10': 0.0,
          'ing_11': 0.0,
          'evaporation': 0.0,
          'pattern': 48},
         'MET+CYS': {'ing_0': 0.0,
          'ing_1': 0.0,
          'ing_2': 0.0,
          'ing_3': 0.0,
          'ing_4': 0.0,
          'ing_5': 0.0,
          'ing_6': 0.0,
          'ing_7': 0.0,
          'ing_8': 0.0,
          'ing_9': 39.0,
          'ing_10': 0.0,
          'ing_11': 0.0,
          'evaporation': 0.0,
          'pattern': 23},
         'PHE+TYR': {'ing_0': 0.0,
          'ing_1': 0.0,
          'ing_2': 0.0,
          'ing_3': 0.0,
          'ing_4': 0.0,
          'ing_5': 0.0,
          'ing_6': 0.0,
          'ing_7': 0.0,
          'ing_8': 0.0,
          'ing_9': 89.9,
          'ing_10': 0.0,
          'ing_11': 0.0,
          'evaporation': 0.0,
          'pattern': 41},
         'THR': {'ing_0': 0.0,
          'ing_1': 0.0,
          'ing_2': 0.0,
          'ing_3': 0.0,
          'ing_4': 0.0,
          'ing_5': 0.0,
          'ing_6': 0.0,
          'ing_7': 0.0,
          'ing_8': 0.0,
          'ing_9': 37.7,
          'ing_10': 0.0,
          'ing_11': 0.0,
          'evaporation': 0.0,
          'pattern': 25},
         'TRP': {'ing_0': 0.0,
          'ing_1': 0.0,
          'ing_2': 0.0,
          'ing_3': 0.0,
          'ing_4': 0.0,
          'ing_5': 0.0,
          'ing_6': 0.0,
          'ing_7': 0.0,
          'ing_8': 0.0,
          'ing_9': 7.1000000000000005,
          'ing_10': 0.0,
          'ing_11': 0.0,
          'evaporation': 0.0,
          'pattern': 6.6},
         'VAL': {'ing_0': 0.0,
          'ing_1': 0.0,
          'ing_2': 0.0,
          'ing_3': 0.0,
          'ing_4': 0.0,
          'ing_5': 0.0,
          'ing_6': 0.0,
          'ing_7': 0.0,
          'ing_8': 0.0,
          'ing_9': 50.7,
          'ing_10': 0.0,
          'ing_11': 0.0,
          'evaporation': 0.0,
          'pattern': 40},
         'HIS': {'ing_0': 0.0,
          'ing_1': 0.0,
          'ing_2': 0.0,
          'ing_3': 0.0,
          'ing_4': 0.0,
          'ing_5': 0.0,
          'ing_6': 0.0,
          'ing_7': 0.0,
          'ing_8': 0.0,
          'ing_9': 30.5,
          'ing_10': 0.0,
          'ing_11': 0.0,
          'evaporation': 0.0,
          'pattern': 16}}}},
      'subcomponents': {},
      'Iumami': {}},
     'optimum': 0.0,
     'reference': 100.0,
     'optimum_cost': 0.0,
     'reference_cost': 15.913521421,
     'lbound': nan,
     'ubound': nan,
     'lslack': nan,
     'uslack': nan},
    'Stage_1': {'recipe': {'ingredients': {'ing_9': {'optimum': 100.0,
        'reference': 0.0,
        'optimum_cost': 1.5,
        'reference_cost': 0.0,
        'lbound': nan,
        'ubound': 100.0,
        'lslack': nan,
        'uslack': 0.0},
       'ing_10': {'optimum': 0.0,
        'reference': 0.0,
        'optimum_cost': 0.0,
        'reference_cost': 0.0,
        'lbound': nan,
        'ubound': 100.0,
        'lslack': nan,
        'uslack': 100.0},
       'ing_11': {'optimum': 0.0,
        'reference': 0.0,
        'optimum_cost': 0.0,
        'reference_cost': 0.0,
        'lbound': nan,
        'ubound': 100.0,
        'lslack': nan,
        'uslack': 100.0}},
      'nutrients': {'sugars': {'optimum': 16.417044103109234,
        'reference': 0.0,
        'lbound': 36.0,
        'ubound': 40.0,
        'lslack': -21.224660307201688,
        'uslack': 25.224660307201688},
       'added sugars': {'optimum': 21.68969768017482,
        'reference': 0.0,
        'lbound': nan,
        'ubound': 42.4,
        'lslack': nan,
        'uslack': 20.71030231982518},
       'protein': {'optimum': 25.496835637093675,
        'reference': 0.0,
        'lbound': 18.0,
        'ubound': nan,
        'lslack': 7.496835637093675,
        'uslack': nan},
       'fiber': {'optimum': 14.329092644518571,
        'reference': 0.0,
        'lbound': 10.0,
        'ubound': 12.0,
        'lslack': 4.329092644518571,
        'uslack': -2.329092644518571},
       'sodium': {'optimum': 34.80078818568087,
        'reference': 0.0,
        'lbound': nan,
        'ubound': 560.0,
        'lslack': nan,
        'uslack': 525.1992118143191},
       'calcium': {'optimum': 46.65770345461839,
        'reference': 0.0,
        'lbound': 58.197387159236385,
        'ubound': nan,
        'lslack': inf,
        'uslack': nan},
       'sfa': {'optimum': 39.89272328550022,
        'reference': 0.0,
        'lbound': nan,
        'ubound': 20.0,
        'lslack': nan,
        'uslack': -19.892723285500217},
       'energy': {'optimum': 55.42608300879656,
        'reference': 0.0,
        'lbound': nan,
        'ubound': 680.0,
        'lslack': nan,
        'uslack': 624.5739169912034},
       'water': {'optimum': 10.662134216781736,
        'reference': 0.0,
        'lbound': nan,
        'ubound': 5.0,
        'lslack': nan,
        'uslack': -5.662134216781736},
       'iron': {'optimum': 6.311278269337809,
        'reference': 0.0,
        'lbound': nan,
        'ubound': nan,
        'lslack': nan,
        'uslack': nan}},
      'sustainability': {'GHGe': {'optimum': 1.25,
        'reference': 0.0,
        'lbound': nan,
        'ubound': 4.0,
        'lslack': nan,
        'uslack': 2.75}},
      'other parameters': {'property_1': {'optimum': 19.0,
        'reference': 0.0,
        'lbound': nan,
        'ubound': 2.5,
        'lslack': nan,
        'uslack': -16.5},
       'property_2': {'optimum': 16.0,
        'reference': 0.0,
        'lbound': 9.0,
        'ubound': nan,
        'lslack': 7.0,
        'uslack': nan}},
      'nutriscore data': {'score': {'optimum': -2.0, 'reference': -2.0},
       'NutriScore': {'optimum': 'B', 'reference': 'B'},
       'score_break_down': {'optimum': {'sugars': {'value': 1.8469174615997888,
          'score': 1.0},
         'protein': {'value': 3.1871044546367093, 'score': 7.0},
         'fiber': {'value': 1.7911365805648214, 'score': 0.0},
         'salt': {'value': 0.010875246308025274, 'score': 0.0},
         'fvpno_eff': {'value': 0.0, 'score': 0.0},
         'sfa': {'value': 4.986590410687527, 'score': 4.0},
         'energy': {'value': 6.92826037609957, 'score': 0.0},
         'nn_sweeteners': {'value': 0.0, 'score': 0.0}},
        'reference': {'sugars': {'value': 4.7819929212887775, 'score': 3.0},
         'protein': {'value': 3.5900727181846097, 'score': 7.0},
         'fiber': {'value': 4.939024415792947, 'score': 2.0},
         'salt': {'value': 0.012574223319731626, 'score': 0.0},
         'fvpno_eff': {'value': 0, 'score': 0.0},
         'sfa': {'value': 3.010573178006309, 'score': 3.0},
         'energy': {'value': 7.719789733072539, 'score': 1.0},
         'nn_sweeteners': {'value': 0, 'score': 0.0}}},
       'version': 'nutriscore_2023'},
      'HSR': {'points': {'optimum': 2.0, 'reference': -4.0},
       'score': {'optimum': 3.5, 'reference': 4},
       'score_break_down': {'optimum': {'sugars': {'value': 1.8469174615997888,
          'score': 0.0},
         'protein': {'value': 3.1871044546367093, 'score': 1.0},
         'fiber': {'value': 1.7911365805648214, 'score': 1.0},
         'sodium': {'value': 4.350098523210109, 'score': 0.0},
         'sfa': {'value': 4.986590410687527, 'score': 4.0},
         'energy': {'value': 6.92826037609957, 'score': 0.0},
         'fv_c': {'value': 0.0, 'score': 0.0},
         'fvnl_nc': {'value': 0.0, 'score': 0.0}},
        'reference': {'sugars': {'value': 4.7819929212887775, 'score': 0.0},
         'protein': {'value': 3.5900727181846097, 'score': 2.0},
         'fiber': {'value': 4.939024415792947, 'score': 5.0},
         'sodium': {'value': 5.02968932789265, 'score': 0.0},
         'sfa': {'value': 3.010573178006309, 'score': 3.0},
         'energy': {'value': 7.719789733072539, 'score': 0.0},
         'fv_c': {'value': 0, 'score': 0.0},
         'fvnl_nc': {'value': 0, 'score': 0.0}}}},
      'PDCAAS data': {'reference': 1.1069565217391304,
       'optimum': 0.511125,
       'AA_breakdown': {'optimum': {'ILE': {'ing_0': 0.0,
          'ing_1': 0.0,
          'ing_2': 0.0,
          'ing_3': 0.0,
          'ing_4': 0.0,
          'ing_5': 0.0,
          'ing_6': 0.0,
          'ing_7': 0.0,
          'ing_8': 0.0,
          'ing_9': 35.8,
          'ing_10': 0.0,
          'ing_11': 0.0,
          'evaporation': 0.0,
          'pattern': 30},
         'LEU': {'ing_0': 0.0,
          'ing_1': 0.0,
          'ing_2': 0.0,
          'ing_3': 0.0,
          'ing_4': 0.0,
          'ing_5': 0.0,
          'ing_6': 0.0,
          'ing_7': 0.0,
          'ing_8': 0.0,
          'ing_9': 122.8,
          'ing_10': 0.0,
          'ing_11': 0.0,
          'evaporation': 0.0,
          'pattern': 61},
         'LYS': {'ing_0': 0.0,
          'ing_1': 0.0,
          'ing_2': 0.0,
          'ing_3': 0.0,
          'ing_4': 0.0,
          'ing_5': 0.0,
          'ing_6': 0.0,
          'ing_7': 0.0,
          'ing_8': 0.0,
          'ing_9': 28.2,
          'ing_10': 0.0,
          'ing_11': 0.0,
          'evaporation': 0.0,
          'pattern': 48},
         'MET+CYS': {'ing_0': 0.0,
          'ing_1': 0.0,
          'ing_2': 0.0,
          'ing_3': 0.0,
          'ing_4': 0.0,
          'ing_5': 0.0,
          'ing_6': 0.0,
          'ing_7': 0.0,
          'ing_8': 0.0,
          'ing_9': 39.0,
          'ing_10': 0.0,
          'ing_11': 0.0,
          'evaporation': 0.0,
          'pattern': 23},
         'PHE+TYR': {'ing_0': 0.0,
          'ing_1': 0.0,
          'ing_2': 0.0,
          'ing_3': 0.0,
          'ing_4': 0.0,
          'ing_5': 0.0,
          'ing_6': 0.0,
          'ing_7': 0.0,
          'ing_8': 0.0,
          'ing_9': 89.9,
          'ing_10': 0.0,
          'ing_11': 0.0,
          'evaporation': 0.0,
          'pattern': 41},
         'THR': {'ing_0': 0.0,
          'ing_1': 0.0,
          'ing_2': 0.0,
          'ing_3': 0.0,
          'ing_4': 0.0,
          'ing_5': 0.0,
          'ing_6': 0.0,
          'ing_7': 0.0,
          'ing_8': 0.0,
          'ing_9': 37.7,
          'ing_10': 0.0,
          'ing_11': 0.0,
          'evaporation': 0.0,
          'pattern': 25},
         'TRP': {'ing_0': 0.0,
          'ing_1': 0.0,
          'ing_2': 0.0,
          'ing_3': 0.0,
          'ing_4': 0.0,
          'ing_5': 0.0,
          'ing_6': 0.0,
          'ing_7': 0.0,
          'ing_8': 0.0,
          'ing_9': 7.1000000000000005,
          'ing_10': 0.0,
          'ing_11': 0.0,
          'evaporation': 0.0,
          'pattern': 6.6},
         'VAL': {'ing_0': 0.0,
          'ing_1': 0.0,
          'ing_2': 0.0,
          'ing_3': 0.0,
          'ing_4': 0.0,
          'ing_5': 0.0,
          'ing_6': 0.0,
          'ing_7': 0.0,
          'ing_8': 0.0,
          'ing_9': 50.7,
          'ing_10': 0.0,
          'ing_11': 0.0,
          'evaporation': 0.0,
          'pattern': 40},
         'HIS': {'ing_0': 0.0,
          'ing_1': 0.0,
          'ing_2': 0.0,
          'ing_3': 0.0,
          'ing_4': 0.0,
          'ing_5': 0.0,
          'ing_6': 0.0,
          'ing_7': 0.0,
          'ing_8': 0.0,
          'ing_9': 30.5,
          'ing_10': 0.0,
          'ing_11': 0.0,
          'evaporation': 0.0,
          'pattern': 16}}}},
      'subcomponents': {},
      'Iumami': {}},
     'optimum': 100.0,
     'reference': 100.0,
     'optimum_cost': 1.5,
     'reference_cost': 0.0,
     'lbound': nan,
     'ubound': nan,
     'lslack': nan,
     'uslack': nan}},
   'nutrients': {'sugars': {'optimum': 14.77533969279831,
     'reference': 38.25594337031022,
     'lbound': 36.0,
     'ubound': 40.0,
     'lslack': -21.224660307201688,
     'uslack': 25.224660307201688},
    'added sugars': {'optimum': 21.68969768017482,
     'reference': 18.893219834808427,
     'lbound': nan,
     'ubound': 42.4,
     'lslack': nan,
     'uslack': 20.71030231982518},
    'protein': {'optimum': 25.496835637093675,
     'reference': 28.720581745476878,
     'lbound': 18.0,
     'ubound': nan,
     'lslack': 7.496835637093675,
     'uslack': nan},
    'fiber': {'optimum': 14.329092644518571,
     'reference': 39.51219532634357,
     'lbound': 10.0,
     'ubound': 12.0,
     'lslack': 4.329092644518571,
     'uslack': -2.329092644518571},
    'sodium': {'optimum': 34.80078818568087,
     'reference': 40.2375146231412,
     'lbound': nan,
     'ubound': 560.0,
     'lslack': nan,
     'uslack': 525.1992118143191},
    'calcium': {'optimum': 46.65770345461839,
     'reference': 29.493064438514818,
     'lbound': 58.197387159236385,
     'ubound': nan,
     'lslack': inf,
     'uslack': nan},
    'sfa': {'optimum': 39.89272328550022,
     'reference': 24.084585424050474,
     'lbound': nan,
     'ubound': 20.0,
     'lslack': nan,
     'uslack': -19.892723285500217},
    'energy': {'optimum': 55.42608300879656,
     'reference': 61.75831786458031,
     'lbound': nan,
     'ubound': 680.0,
     'lslack': nan,
     'uslack': 624.5739169912034},
    'water': {'optimum': 10.662134216781736,
     'reference': 49.224707679959764,
     'lbound': nan,
     'ubound': 5.0,
     'lslack': nan,
     'uslack': -5.662134216781736},
    'iron': {'optimum': 6.311278269337809,
     'reference': 39.970132028473884,
     'lbound': nan,
     'ubound': nan,
     'lslack': nan,
     'uslack': nan}},
   'sustainability': {'GHGe': {'optimum': 1.25,
     'reference': 5.310106028105906,
     'lbound': nan,
     'ubound': 4.0,
     'lslack': nan,
     'uslack': 2.75}},
   'other parameters': {'property_1': {'optimum': 19.0,
     'reference': 13.412770968467658,
     'lbound': nan,
     'ubound': 2.5,
     'lslack': nan,
     'uslack': -16.5},
    'property_2': {'optimum': 16.0,
     'reference': 3.898621033424167,
     'lbound': 9.0,
     'ubound': nan,
     'lslack': 7.0,
     'uslack': nan}},
   'nutriscore data': {'score': {'optimum': -2.0, 'reference': -2.0},
    'NutriScore': {'optimum': 'B', 'reference': 'B'},
    'score_break_down': {'optimum': {'sugars': {'value': 1.8469174615997888,
       'score': 1.0},
      'protein': {'value': 3.1871044546367093, 'score': 7.0},
      'fiber': {'value': 1.7911365805648214, 'score': 0.0},
      'salt': {'value': 0.010875246308025274, 'score': 0.0},
      'fvpno_eff': {'value': 0.0, 'score': 0.0},
      'sfa': {'value': 4.986590410687527, 'score': 4.0},
      'energy': {'value': 6.92826037609957, 'score': 0.0},
      'nn_sweeteners': {'value': 0.0, 'score': 0.0}},
     'reference': {'sugars': {'value': 4.7819929212887775, 'score': 3.0},
      'protein': {'value': 3.5900727181846097, 'score': 7.0},
      'fiber': {'value': 4.939024415792947, 'score': 2.0},
      'salt': {'value': 0.012574223319731626, 'score': 0.0},
      'fvpno_eff': {'value': 0, 'score': 0.0},
      'sfa': {'value': 3.010573178006309, 'score': 3.0},
      'energy': {'value': 7.719789733072539, 'score': 1.0},
      'nn_sweeteners': {'value': 0, 'score': 0.0}}},
    'version': 'nutriscore_2023'},
   'HSR': {'points': {'optimum': 2.0, 'reference': -4.0},
    'score': {'optimum': 3.5, 'reference': 4},
    'score_break_down': {'optimum': {'sugars': {'value': 1.8469174615997888,
       'score': 0.0},
      'protein': {'value': 3.1871044546367093, 'score': 1.0},
      'fiber': {'value': 1.7911365805648214, 'score': 1.0},
      'sodium': {'value': 4.350098523210109, 'score': 0.0},
      'sfa': {'value': 4.986590410687527, 'score': 4.0},
      'energy': {'value': 6.92826037609957, 'score': 0.0},
      'fv_c': {'value': 0.0, 'score': 0.0},
      'fvnl_nc': {'value': 0.0, 'score': 0.0}},
     'reference': {'sugars': {'value': 4.7819929212887775, 'score': 0.0},
      'protein': {'value': 3.5900727181846097, 'score': 2.0},
      'fiber': {'value': 4.939024415792947, 'score': 5.0},
      'sodium': {'value': 5.02968932789265, 'score': 0.0},
      'sfa': {'value': 3.010573178006309, 'score': 3.0},
      'energy': {'value': 7.719789733072539, 'score': 0.0},
      'fv_c': {'value': 0, 'score': 0.0},
      'fvnl_nc': {'value': 0, 'score': 0.0}}}},
   'PDCAAS data': {'reference': 1.1069565217391304,
    'optimum': 0.511125,
    'AA_breakdown': {'optimum': {'ILE': {'ing_0': 0.0,
       'ing_1': 0.0,
       'ing_2': 0.0,
       'ing_3': 0.0,
       'ing_4': 0.0,
       'ing_5': 0.0,
       'ing_6': 0.0,
       'ing_7': 0.0,
       'ing_8': 0.0,
       'ing_9': 35.8,
       'ing_10': 0.0,
       'ing_11': 0.0,
       'evaporation': 0.0,
       'pattern': 30},
      'LEU': {'ing_0': 0.0,
       'ing_1': 0.0,
       'ing_2': 0.0,
       'ing_3': 0.0,
       'ing_4': 0.0,
       'ing_5': 0.0,
       'ing_6': 0.0,
       'ing_7': 0.0,
       'ing_8': 0.0,
       'ing_9': 122.8,
       'ing_10': 0.0,
       'ing_11': 0.0,
       'evaporation': 0.0,
       'pattern': 61},
      'LYS': {'ing_0': 0.0,
       'ing_1': 0.0,
       'ing_2': 0.0,
       'ing_3': 0.0,
       'ing_4': 0.0,
       'ing_5': 0.0,
       'ing_6': 0.0,
       'ing_7': 0.0,
       'ing_8': 0.0,
       'ing_9': 28.2,
       'ing_10': 0.0,
       'ing_11': 0.0,
       'evaporation': 0.0,
       'pattern': 48},
      'MET+CYS': {'ing_0': 0.0,
       'ing_1': 0.0,
       'ing_2': 0.0,
       'ing_3': 0.0,
       'ing_4': 0.0,
       'ing_5': 0.0,
       'ing_6': 0.0,
       'ing_7': 0.0,
       'ing_8': 0.0,
       'ing_9': 39.0,
       'ing_10': 0.0,
       'ing_11': 0.0,
       'evaporation': 0.0,
       'pattern': 23},
      'PHE+TYR': {'ing_0': 0.0,
       'ing_1': 0.0,
       'ing_2': 0.0,
       'ing_3': 0.0,
       'ing_4': 0.0,
       'ing_5': 0.0,
       'ing_6': 0.0,
       'ing_7': 0.0,
       'ing_8': 0.0,
       'ing_9': 89.9,
       'ing_10': 0.0,
       'ing_11': 0.0,
       'evaporation': 0.0,
       'pattern': 41},
      'THR': {'ing_0': 0.0,
       'ing_1': 0.0,
       'ing_2': 0.0,
       'ing_3': 0.0,
       'ing_4': 0.0,
       'ing_5': 0.0,
       'ing_6': 0.0,
       'ing_7': 0.0,
       'ing_8': 0.0,
       'ing_9': 37.7,
       'ing_10': 0.0,
       'ing_11': 0.0,
       'evaporation': 0.0,
       'pattern': 25},
      'TRP': {'ing_0': 0.0,
       'ing_1': 0.0,
       'ing_2': 0.0,
       'ing_3': 0.0,
       'ing_4': 0.0,
       'ing_5': 0.0,
       'ing_6': 0.0,
       'ing_7': 0.0,
       'ing_8': 0.0,
       'ing_9': 7.1000000000000005,
       'ing_10': 0.0,
       'ing_11': 0.0,
       'evaporation': 0.0,
       'pattern': 6.6},
      'VAL': {'ing_0': 0.0,
       'ing_1': 0.0,
       'ing_2': 0.0,
       'ing_3': 0.0,
       'ing_4': 0.0,
       'ing_5': 0.0,
       'ing_6': 0.0,
       'ing_7': 0.0,
       'ing_8': 0.0,
       'ing_9': 50.7,
       'ing_10': 0.0,
       'ing_11': 0.0,
       'evaporation': 0.0,
       'pattern': 40},
      'HIS': {'ing_0': 0.0,
       'ing_1': 0.0,
       'ing_2': 0.0,
       'ing_3': 0.0,
       'ing_4': 0.0,
       'ing_5': 0.0,
       'ing_6': 0.0,
       'ing_7': 0.0,
       'ing_8': 0.0,
       'ing_9': 30.5,
       'ing_10': 0.0,
       'ing_11': 0.0,
       'evaporation': 0.0,
       'pattern': 16}}}},
   'subcomponents': {},
   'Iumami': {},
   'cost': 1.5,
   'optimum_cost': 1.5,
   'reference_cost': 15.913521421,
   'unit_cost': 'USD/kg'}}}

```

## Example corresponding output ```constraints_loosen_slacks```

```python

[{'constraint name': 'sugars lower',
  'slack value': -21.224660307201688,
  'constraint value': 36.0,
  'per': '100g'},
 {'constraint name': 'fiber upper',
  'slack value': 2.329092644518571,
  'constraint value': 12.0,
  'per': '100g'},
 {'constraint name': 'calcium lower',
  'slack value': -20.81995168734287,
  'constraint value': 105.0,
  'per': '100kcal'},
 {'constraint name': 'sfa upper',
  'slack value': 2.486590410687527,
  'constraint value': 2.5,
  'per': '100ml'},
 {'constraint name': 'water nut upper',
  'slack value': 5.662134216781736,
  'constraint value': 5.0,
  'per': '100g'},
 {'constraint name': 'property 1 upper',
  'slack value': 16.5,
  'constraint value': 2.5,
  'per': '100g'},
 {'constraint name': 'class_2 + class_3 lower',
  'slack value': -0.2,
  'constraint value': 0.2,
  'per': '100g'}]

```
