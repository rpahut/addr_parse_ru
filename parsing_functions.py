import re
from fuzzywuzzy import fuzz
from preparsing_functions import generate_ngrams


def extract_address_part(s, names, order_list=(3, 2, 1), types=tuple(), special_names=tuple()):
    ret_grams = []
    first_loop = True
    # i = 0
    for n in order_list:
        grams_list = generate_ngrams(s, n)
        for gram in grams_list:
            # i += 1
            # print(str(n) + " номер " + str(i) +" "+ gram)
            name_value = ""
            contains_name = False
            contains_type = False
            contains_period = False
            if n == 1:
                contains_type = True
            if n < 3:
                contains_period = True
            for word in gram.split():
                if word in special_names and n == 1:
                    return " ".join(ret_grams), s
                if word in names or word in special_names:
                    contains_name = True
                    name_value = word
                if word in types:
                    contains_type = True
                if word == ".":
                    contains_period = True
            # print(nam)
            # print(typ)
            # print(punct)
            # print("--------")
            if contains_name & contains_type & contains_period & (first_loop or name_value in ret_grams):
                s = re.sub(gram, "", s, flags=re.IGNORECASE, count=1)
                ret_grams.extend(g for g in gram.split() if g not in ret_grams)
                first_loop = False
    return " ".join(ret_grams), s

def extract_town_fuzzy(text, towns):
    """
    отделить от текста первое из слов, достаточно близко совпадающее с одним из списка
    """
    end_list = ("ий", "ый", "ая", "яя", "ое", "ее", "ой", "ва", "на", "са", "ма")
    remainder = list()
    still_looking = True
    close_matching_name = ""
    for word in text.lower().split():
        if still_looking and (word[-2:] not in end_list or word[-2:] == "ва" and fuzz.ratio(word, "москва") >= 90):
            for town in towns:
                if fuzz.ratio(word, town.lower()) >= 90:
                    print('Fuzzy match "' + word + '" ---> "' + town + '" in text ' + text)
                    still_looking = False
                    close_matching_name = town
            if still_looking:
                remainder.append(word)
        else:
            remainder.append(word)
    return close_matching_name, " ".join(remainder)
