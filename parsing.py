from preparsing_functions import normalize_punctuation, collapse_spaces, dict_replace_caseless, dict_replace_caseless_multiword
from preparsing import towns_to_singleword_map, settlements_to_singleword_map, towns_list, regions_list, settlements_list, towns_singleword_only, settlements_adjf
from constants import COUNTRY_KEY_WORDS, TOWNS_KEY_WORDS, SPECIAL_TOWNS, REGIONS_KEY_WORDS, SPECIAL_REGIONS, SETTLEMENT_KEY_WORDS
from parsing_functions import extract_address_part, extract_town_fuzzy
from postparsing_functions import concat_alternatives, collapse_punctuation, invoke_if_empty, yargy_parse_street_name_only, parse_street_fallback, parse_building_number_if_empty, normalize_capitalization, keep_alphanum, drop_punct, normalize_town_name, expand_settlement_abbreviation, normalize_settlement_name, special_parse_officen, normalize_office_dot
from parser_func import yargy_parse_region, yargy_parse_okrug, yargy_parse_district, yargy_parse_settlement, yargy_parse_street, yargy_parse_building, yargy_parse_index, yargy_parse_place


def preprocess_address_text(address):
    address = normalize_punctuation(address)
    address = collapse_spaces(address)
    # print(address)
    address = dict_replace_caseless(address, dictionary={'ё': 'е', ' р . п . ': ' рп ', 'р . п ': 'рп ', ' р п ': ' рп '})
    # print(address)
    address = dict_replace_caseless_multiword(address, change_dict=towns_to_singleword_map)
    address = dict_replace_caseless_multiword(address, change_dict=settlements_to_singleword_map)
    address = address.replace('МО', 'Московская область')
    return address

def parse_settlement(address, fuzzy_match_town = True):
    """
    Выделить из текста и вернуть название города или послеления.
    Если флаг fuzzy_match_town установлен, может использоваться поиск названия города по нечёткому совпадению. Совпадение проверяется со списком предопределённых названий (только однословные названия). Нечёткое сравнение позволяет обнаруживать в тексте название города даже в ошибочной записи, если заранее известно что оно есть. Нечёткое сравнение значительно увеличивает время выполнения.
    """
    address = preprocess_address_text(address)
    gorod, addr_remainder = extract_address_part(s=address, names=towns_list, types=TOWNS_KEY_WORDS, special_names=SPECIAL_TOWNS)
    poselenie = ''
    guessed_poselenie = None
    if gorod == '':
        poselenie, addr_remainder = extract_address_part(s=addr_remainder, names=settlements_list, order_list=(2, 3, 1), types=SETTLEMENT_KEY_WORDS, special_names=settlements_adjf)
        if poselenie == '':
            # yargy пытается нащупать название, но нет гарантий что шаблон будет работать в каждом случае, поэтому предпочитаем обнаружение имени по списку
            # FIXME буква 'с' в произвольном тексте принимается за сокращение от село, шаблон возвращает "село учётом ситуации" "село удовольствием"
            poselenie, addr_remainder = yargy_parse_settlement(addr_remainder)
            if poselenie != '':
                guessed_poselenie = poselenie
    if gorod == '' and poselenie == '' and fuzzy_match_town:
        gorod, addr_remainder = extract_town_fuzzy(addr_remainder, towns=towns_singleword_only)
    if gorod != '':
        gorod = normalize_capitalization(gorod)
        gorod = drop_punct(gorod)
        gorod = normalize_town_name(gorod)
        return gorod
    poselenie = normalize_capitalization(poselenie)
    poselenie = drop_punct(poselenie)
    poselenie = expand_settlement_abbreviation(poselenie)
    poselenie = normalize_settlement_name(poselenie)
    return poselenie, guessed_poselenie

def parse_address(address, fuzzy_match_town = True):
    """
    Извлечь из строки адреса составные части.
    Возвращает обнаруженные части адреса в нормализованной форме.

    То что этой функции называется town - на самом деле город (по российским нормам это 20тыс+ жителей), а settlement - это любое село, посёлок или деревня. Значение всегда будет только в одном поле или другом, никогда в обоих. То есть, town и settlement вместе определяют населённый пункт из адреса, возвращаются в разных полях только для того чтобы их можно было различить.
    """
    address = preprocess_address_text(address)
    index, addr_remainder = yargy_parse_index(address)
    # print(address)
    country, addr_remainder = extract_address_part(s=addr_remainder, order_list=(1,), names=COUNTRY_KEY_WORDS)
    # print("ost1: " + ost)
    # print(towns_list)
    town, addr_remainder = extract_address_part(s=addr_remainder, names=towns_list, types=TOWNS_KEY_WORDS, special_names=SPECIAL_TOWNS)
    # print("ost2: " + ost)
    region, addr_remainder = extract_address_part(s=addr_remainder, names=regions_list, types=REGIONS_KEY_WORDS, special_names=SPECIAL_REGIONS)
    # print("ost3: " + ost)
    settlement = ''
    if town == '':
        settlement, addr_remainder = extract_address_part(s=addr_remainder, names=settlements_list, order_list=(2, 3, 1), types=SETTLEMENT_KEY_WORDS, special_names=settlements_adjf)
    # print("ost3.5: " + ost)
    if town == '' and settlement == '' and fuzzy_match_town:
        town, addr_remainder = extract_town_fuzzy(addr_remainder, towns=towns_singleword_only)

    region_yargy, addr_remainder = yargy_parse_region(addr_remainder)
    okrug_yargy, addr_remainder = yargy_parse_okrug(addr_remainder)
    district, addr_remainder = yargy_parse_district(addr_remainder)
    settlement_yargy, addr_remainder = yargy_parse_settlement(addr_remainder)
    street, addr_remainder = yargy_parse_street(addr_remainder)
    building, addr_remainder = yargy_parse_building(addr_remainder)
    place, addr_remainder = yargy_parse_place(addr_remainder)

    # print("ost4: " + ost)
    region = concat_alternatives(region, region_yargy)
    settlement = concat_alternatives(settlement, settlement_yargy)
    addr_remainder = collapse_punctuation(addr_remainder)
    street, addr_remainder = invoke_if_empty(street, addr_remainder, func=yargy_parse_street_name_only)
    # print("ost5: " + ost)
    street, addr_remainder = invoke_if_empty(street, addr_remainder, func=parse_street_fallback)
    # print("ost6: " + ost)
    building, addr_remainder = parse_building_number_if_empty(building, addr_remainder)

    addr_remainder = keep_alphanum(addr_remainder)

    place, addr_remainder = special_parse_officen(place, addr_remainder)
    place = normalize_office_dot(place)

    country = normalize_capitalization(country)
    country = keep_alphanum(country)
    region = normalize_capitalization(region)
    region = drop_punct(region)
    town = normalize_capitalization(town)
    town = drop_punct(town)
    town = normalize_town_name(town)
    settlement = normalize_capitalization(settlement)
    settlement = drop_punct(settlement)
    settlement = expand_settlement_abbreviation(settlement)
    settlement = normalize_settlement_name(settlement)
    district = normalize_capitalization(district)
    street = normalize_capitalization(street)
    building = normalize_capitalization(building)
    place = normalize_capitalization(place)

    return country, region, town, settlement, district, street, building, place, index
