import re
from constants import ALL_KEY_WORDS, KEY_WORDS_DICT
from yargy_rules.street_only import street_name_only_parser

# объединить части адреса в строку через запятую
def join_addr_parts(*addr_parts):
    res = list()
    for addr_part in addr_parts:
        if addr_part != "":
            res.append(str(addr_part))
    return ", ".join(res)


def normalize_office_dot(s):
    if s.find(' . ') < 0:
        return s
    return s.replace(' . ', '.')


def is_punct(s):
    s = re.sub(',+', '', s)
    s = re.sub(r'\.+', '', s)
    if s == "":
        return True
    else:
        return False


def collapse_punctuation(text):
    res = list()
    for word in text.split():
        if res:
            if (res[-1] != ',' and res[-1] != '.') or not is_punct(word):
                word = re.sub(',+', ',', word)
                word = re.sub(r'\.+', '.', word)
                res.append(word)
        elif not is_punct(word):
            res.append(word)
    return " ".join(res)

# извлечь из текста название улицы
def yargy_parse_street_name_only(text):
    parser=street_name_only_parser
    street = ""
    for match in parser.findall(text):
        text = text[0: match.span.start] + text[match.span.stop:]
        street = "улица " + match.fact.value
        try:
            value, span, typ, forms = [x for x in match.tokens[0]]
            name, grams = forms[0]
            gen = grams.gender
            male, female, neutral, bi, general = [x for x in gen]
            if male:
                street = "проспект " + match.fact.value
            elif neutral:
                street = "шоссе " + match.fact.value
        except:
            pass
        break
    return street, text


def invoke_if_empty(target, text, func):
    if target == '' and text != '':
        return func(text)
    return target, text

# аварийный способ извлечения названия улицы, используемый только если все другие провалились
# извлечь первое слово, которое может быть названием чего-то, и использовать его как название улицы
def parse_street_fallback(text):
    remainder = list()
    street = ""
    for word in text.split():
        if (len(word) > 2) and word[0].isalpha() and word[1].isalpha() and not street and not word.lower() in ALL_KEY_WORDS:
            street = word
        else:
            remainder.append(word)
    if street != "":
        street = "улица " + street
    return street, " ".join(remainder)

# извлечь из текста первое слово, которое является числом
def parse_building_number(text):
    remainder = list()
    num = ""
    for word in text.split():
        if word[0].isnumeric() and not num:
            num = word
        else:
            remainder.append(word)
    return num, " ".join(remainder)

# извлечь номер дома, если он ещё не известен
def parse_building_number_if_empty(building, text):
    if text == "" or "дом" in building.split():
        return building, text
    else:
        num, text = parse_building_number(text)
        if num != "":
            building = "дом " + num + " " + building
        return building, text


ABBR_UPPER = ("рф", "ао", "осб", "госб", "всп", "до", "удо", "сдо", "дф", "бц", "всп/до", "жк", "мэз")

def normalize_capitalization(text):
    res = list()
    for word in text.lower().split():
        if word.lower() in ABBR_UPPER:
            res.append(word.upper())
        elif word not in ALL_KEY_WORDS:
            if "-" in word:
                subword = word.split("-")
                if subword[0].isnumeric() and subword[1] == 'я':
                    res.append(word)
                else:
                    subword = map(str.capitalize, subword)
                    res.append("-".join(subword))
            elif "_" in word:
                subword = word.split("_")
                subword = map(str.capitalize, subword)
                res.append(" ".join(subword))
            else:
                res.append(word.capitalize())
        else:
            if not KEY_WORDS_DICT.get(word):
                res.append(word)
            else:
                res.append(KEY_WORDS_DICT.get(word))
    return " ".join(res)


def drop_punct(s):
    return s.replace(".", "").replace(",", "")


def expand_settlement_abbreviation(text):
    """
    Функция разворачивает сокращение 'с' или 'п', если они есть в тектсе, в 'село' и 'посёлок' соответственно.
    """
    res = list()
    settlements_dict = {"с": "село", "п": "поселок"}
    for word in text.split():
        if settlements_dict.get(word):
            res.append(settlements_dict.get(word))
        else:
            res.append(word)
    return " ".join(res)


def normalize_town_name(text):
    """
    Текст очищается от всех ключевых слов, перечисленных в ALL_KEY_WORDS. Оставшиеся слова считаются названием города, к нему приставляется слово "город".
    """
    name = list()
    for word in text.split():
        if word not in ALL_KEY_WORDS:
            name.append(word)
    if not name:
        return ""
    return "город" + " " + " ".join(name)


def normalize_settlement_name(s):
    """
    Текст очищается от всех ключевых слов, перечисленных в ALL_KEY_WORDS; при этом последнее убранное ключевое слово запоминается. Оставшиеся слова считаются названием поселения, к нему приставляется запомненное ключевое слово, если не пустое.
    """
    key_word = ""
    name = list()
    for word in s.split():
        if word in ALL_KEY_WORDS:
            key_word = word
        else:
            name.append(word)
    if not name:
        return ""
    if not key_word:
        return " ".join(name)
    else:
        return key_word + " " + " ".join(name)


def keep_alphanum(text):
    res = list()
    for word in text.split():
        if word.isalnum() and word != " " and word != "":
            res.append(word)
    return " ".join(res)

# извлечь номер кабинета для особого случая когда рабочее место ещё не определено и в тексте остался только номер кабинета
def special_parse_officen(place, text):
    if text.isnumeric() and not ("комната" in place.split() or "кабинет" in place.split()):
        if place == "":
            return "кабинет " + text, ""
        return place + " кабинет " + text, ""
    return place, text

def concat_alternatives(s1, s2):
    if s1 and s2:
        return s1 + "|" + s2
    elif s2:
        return s2
    return s1
