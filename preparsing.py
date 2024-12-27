from constants import REGION_NAMES, TOWN_NAMES, SETTLEMENT_NAMES, SINGLEWORD_SETTLEMENTS_TO_REMOVE, MULTIWORD_SETTLEMENTS_TO_REMOVE
from preparsing_functions import separate_multiword_names, separate_adjf_names, make_locality_dict

settlements_singleword_only, settlements_multiword_only = separate_multiword_names(SETTLEMENT_NAMES) # external_settlements принимает значение в global_variables.py
settlements_other, settlements_adjf = separate_adjf_names(settlements_singleword_only)

for elem in list(SINGLEWORD_SETTLEMENTS_TO_REMOVE):
    if elem in settlements_other:
        settlements_other.remove(elem)

for elem in list(MULTIWORD_SETTLEMENTS_TO_REMOVE):
    if elem in settlements_multiword_only:
        settlements_multiword_only.remove(elem)

towns_singleword_only, towns_multiword_only = separate_multiword_names(TOWN_NAMES) # external_towns принимает значение в global_variables.py
towns_to_singleword_map = make_locality_dict(towns_multiword_only) # словарь содержит беспробельные идентификаторы для каждого города

settlements_to_singleword_map = make_locality_dict(settlements_multiword_only) # словарь содержит беспробельные идентификаторы для каждого поселения
settlements_to_singleword_map.update({"автономный округ": "автономный_округ",
                                 "автономная область": "автономная_область",
                                 "северная осетия": "северная_осетия",
                                 "н . новгород": "нижний_новгород",
                                 "в . новгород": "великий_новгород",
                                 "н новгород": "нижний_новгород",
                                 "в новгород": "великий_новгород"})
multiword_settlements_list = list(settlements_to_singleword_map.values())
settlements_other = tuple(settlements_other)
multiword_settlements_list = tuple(multiword_settlements_list)
settlements_list = settlements_other + multiword_settlements_list # settlements_list содержит однословные имена и многословные приведённые к однословной форме

towns_list = list(towns_to_singleword_map.values()) + towns_singleword_only # towns_list содержит однословные имена и многословные приведённые к однословной форме

regions_list = REGION_NAMES # регионы на данный момент не требуют дополнительной обработки