import pandas as pd
from momo.model import MoMoModel
from momo.system_models.system_models import SystemModel, MultiSystemModel
from momo.prototype import Prototype


dbms = SystemModel("DBMS")
dbms.add_feature("Security", {"MySQL": 1, "MS SQL": 1, "Oracle": 1})
dbms.add_feature("Performance", [1, 1, 1])
dbms.add_feature("Speed", [0, 1, 1])

connector = SystemModel("Connector")
connector.add_feature("Flexibility", {"Copper": 1, "Aluminum": 1})
connector.add_feature("Cost", {"Copper": 1, "Aluminum": 1})

model = MoMoModel([dbms])

print(model.get_prototype())

# multi_system_model = MultiSystemModel([dbms, connector])
# expected_combinations = pd.DataFrame(data={
#     ("DBMS", "Security"): [1, 1, 1, 1, 1, 1],
#     ("DBMS", "Performance"): [1, 1, 1, 1, 1, 1],
#     ("DBMS", "Speed"): [0, 0, 1, 1, 1, 1],
#     ("Connector", "Flexibility"): [1, 1, 1, 1, 1, 1],
#     ("Connector", "Cost"): [1, 1, 1, 1, 1, 1],
# }, index=[('MySQL', 'Copper'), ('MySQL', 'Aluminum'),
#           ('MS SQL', 'Copper'), ('MS SQL', 'Aluminum'),
#           ('Oracle', 'Copper'), ('Oracle', 'Aluminum'),])

# print(expected_combinations)
# print(multi_system_model.get_all_combinations().transpose())
# save = multi_system_model.get_all_combinations() == expected_combinations.transpose()

# print(save)

# save.to_csv("save.csv")


# print(Prototype([1, 1], ["Security", "Performance"]))
