import os

COUNTRY_KEY_WORDS = ("страна", "россия", "рф")

REGIONS_KEY_WORDS = ("республика", "респ", "рес", "р-ка", "округ", "область", "обл", "об",
                     "край", "ао", "автономный_округ", "автономная_область", "об-ть", "обл-ть")

SPECIAL_REGIONS = ("краснодарский", "ростовская", "алтайский", "владимирская",
                   "московская", "нижегородская", "приморский", "калининградская",
                   "калужская", "кировская", "вологодская", "пензенская", "амурская",
                   "ставропольский", "ленинградская", "воронежская", "орловская",
                   "новгородская", "смоленская", "псковская", "ивановская", "волгоградская",
                   "ярославская", "курганская", "липецкая", "курская", "самарская", "тамбовская",
                   "тюменская", "омская", "рязанская", "магаданская", "тульская", "тверская",
                   "удмуртская", "брянская", "камчатский")

TOWNS_KEY_WORDS = ("г", "гор", "город")
SPECIAL_TOWNS = ('октябрьский',)

SETTLEMENT_KEY_WORDS = ("село", "с", "сл", "деревня", "дер", "поселок", "посёлок", "п",
                        "пос", "рп", "пгт", "ст", "ст-ца", "станица")
SINGLEWORD_SETTLEMENTS_TO_REMOVE = ("пушкина", "ленина", "новгород", "разина", "революции", "люксембург",
                         "энтузиастов", "ермакова", "мира", "чапаев", "ряд", "улица",
                         "кирова", "гагарина", "энгельса", "калинина", "саха", "фрунзе", "бульвар", "ком", "строение")
SETTLEMENTS_TO_ADD = ("Зеленоград", "Винсады", "Вольск-18", "Волочаевка-2")
MULTIWORD_SETTLEMENTS_TO_REMOVE = ("большая дмитровка", "1 мая", "8 марта", "карла маркса",
                                 "красный путь", "розы люксембург", "степана разина", "красный октябрь",
                                 "льва толстого", "красная площадь", "красные зори", "большая покровская",
                                 "максима горького", "красная пресня", "золотая долина")

RAION_KEY_WORDS = ('р-он', 'р-н', 'район')

STREETS_KEY_WORDS = ("улица", "ул", "пр", "проспект", "пр-кт", "пр-т", "проезд", "пр-зд", "пр-д", "тупик", "туп",
                     "переулок", "пер", "площадь", "пл", "ш", "шоссе", "набережная", "наб", "бульвар",
                     "б-р", "б", "бул", "бр")

KEY_WORDS_DICT = {"ул": "улица", "пр": "проспект", "пр-кт": "проспект", "пр-зд": "проезд",
                  "пр-д": "проезд", "туп": "тупик", "пер": "переулок", "пл": "площадь", "наб": "набережная",
                  "б-р": "бульвар", "бул": "бульвар", "бр": "бульвар",
                  "обл": "область", "рес": "республика", "респ": "республика", "р-ка": "республика",
                  "об-ть": "область", "об": "область", "обл-ть": "область", "о-г": "округ",
                  "автономный_округ": "АО", "гор": "город", "дер": "деревня", "комн": "комната",
                  "корп": "корпус", "мкр": "микрорайон", "пос": "поселок", "р-н": "район",
                  "сл": "село", "ст-ца": "станица"}

BUILDING_KEY_WORDS = ('дом', 'корп', 'место', 'ВСП/ДО', 'кор', 'корпус', 'стр', 'строение', 'оф', 'офис',
                      'кв', 'квартира', 'этаж', 'бц', 'блок', 'башня', 'сектор', 'помещение', 'пом', 'секция',
                      'комната', 'кабинет', 'ком', 'комн', 'ряд', 'окно', 'отделение', 'ОСБ', 'ГОСБ', 'ВСП',
                      'ДО', 'УДО', 'СДО', 'ДФ', 'мрн', 'мкр', 'район', 'микрорайон', 'ВСП/ДО')

ALL_KEY_WORDS = REGIONS_KEY_WORDS + TOWNS_KEY_WORDS + SETTLEMENT_KEY_WORDS +\
            STREETS_KEY_WORDS + BUILDING_KEY_WORDS + RAION_KEY_WORDS

def read_external_names_lists():
    ext_const_dir = os.path.join(os.path.dirname(__file__), "external_constants")
    with open(os.path.join(ext_const_dir, 'towns.txt'), 'r', encoding='utf-8') as f:
        towns = f.read()

    towns = towns.split(",")

    with open(os.path.join(ext_const_dir, 'regions.txt'), 'r', encoding='utf-8') as f:
        regions = f.read()

    regions = regions.split(",")

    with open(os.path.join(ext_const_dir, 'settlements.txt'), 'r', encoding='utf-8') as f:
        settlements = f.read()  # это как-то надо вынести, чтобы каждый раз не выполнялось чтение файлов

    settlements = settlements.split(",")

    with open(os.path.join(ext_const_dir, 'districts.txt'), 'r', encoding='utf-8') as f:
        districts = f.read()
    districts = districts.split(',')

    return towns, regions, settlements, districts

TOWN_NAMES, REGION_NAMES, SETTLEMENT_NAMES, DISTRICT_NAMES = read_external_names_lists()
