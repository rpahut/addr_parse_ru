import re


def normalize_punctuation(s):
    return s.replace(".", " . ").replace(",", " , ").replace(")", "").replace("(", "")


def collapse_spaces(s):
    return re.sub(' +', ' ', s)

# заменяет в тексте каждое точное совпадение ключа на соотвтствующее значение по словарю
def dict_replace_caseless(text, dictionary):
    for key, replacement in dictionary.items():
        text = re.sub(key, replacement, text, flags=re.IGNORECASE)
    return text

# заменяет в тексте сложные совпадения ключа из трёх, двух или одного слова, начиная с более длинных, на соответствующее значение по словарю
def dict_replace_caseless_multiword(text, change_dict):
    for i in range(3, 0, -1):
        grams_list = generate_ngrams(text, i)
        for gram in grams_list:
            # print(gram)
            if change_dict.get(gram):
                return re.sub(gram, change_dict.get(gram), text, flags=re.IGNORECASE)
    return text

# сгенерировать из слов текста пересекающиеся n-граммы, по n слов каждая
def generate_ngrams(text, n):
    text = text.lower()
    text = re.sub(r'^[a-zA-Z0-9,.\s]', ' ', text)
    tokens = [token for token in text.split(" ") if token != ""]
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]


# формирует словарь, в котором каждому имени из заданного списка сопоставляется идентификатор без пробелов и скобок
def make_locality_dict(locs):
    l_dict = {}
    for loc in locs:
        if len(re.split(r'[\s]\s*', loc)) > 1:
            name = re.sub(r'\([^()]*\)', "", loc, flags=re.IGNORECASE) # удаляем любое содержимое в скобках
            name = re.split(r'[\s]\s*', name)
            if "" in name:
                name.remove("")
            if " " in name:
                name.remove(" ")
            l_dict.update({loc: "_".join(name)})
    return l_dict


def separate_multiword_names(locations):
    single = list()
    multi = list()
    for loc in locations:
        if len(loc.split()) > 1:
            multi.append(loc)
        else:
            single.append(loc)
    return single, multi

# отделяет прилагательно-подобные имена (по окончаниям) в отдельный список
def separate_adjf_names(locations):
    other = list()
    adjf = list()
    end_list = ("ий", "ый", "ая", "яя", "ое", "ее", "ой", "ва")
    for loc in locations:
        if loc[-2:] in end_list:
            adjf.append(loc)
        else:
            other.append(loc)
    return other, adjf
