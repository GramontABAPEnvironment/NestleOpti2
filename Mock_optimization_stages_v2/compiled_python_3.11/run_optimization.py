from mock_model_definition import create_and_solve_model

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

results_dict, constraints_loosen_slacks, no_loosen, out_message, instance = create_and_solve_model(**data)


print(results_dict)