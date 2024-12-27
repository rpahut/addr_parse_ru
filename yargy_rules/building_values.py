from yargy_rules.streets import ADDR_VALUE
from value_func import value
from yargy_rules.common import *
from yargy.tokenizer import MorphTokenizer, TokenRule, RULES


###########
#
#   DOM_FULL_NUM
#
#############


Building = fact(
	'Building',
	['primary', 'korpus', 'stroenie']
)

class Building(Building):
	def to_string(self):
		ret = None
		if self.primary:
			ret = 'дом ' + str(self.primary)
			if self.korpus:
				ret += ' корпус ' + str(self.korpus)
			if self.stroenie:
				ret += ' строение ' + str(self.stroenie)
		return ret

reusable_building_tokenizer = None

def make_building_tokenizer():
	"""
	создать специальный токенизатор конкретно для номеров домов
	"""
	global reusable_building_tokenizer
	if not reusable_building_tokenizer:
		# текстовыми токенами могут быть только отдельные буквы и ключевые слова
		tokrule_special = TokenRule(
			type='RU',
			pattern='[абвгдежзийлмнопртуфхшщэюя]|дом|д|корпус|корп|к|строение|стр|ст|с'
		)

		reusable_building_tokenizer = MorphTokenizer(RULES)
		reusable_building_tokenizer.remove_types('RU')
		reusable_building_tokenizer.add_rules(tokrule_special)
	return reusable_building_tokenizer

DOM_NUMBER_LETTER = in_caseless(set('абвгдежзийлмнопртуфхшщэюя')) # без к и с

DOM_PRIMARY_NUM = rule(
    in_caseless({'дом', 'д', ''}).optional(),
	DOT.optional(), # точка это отдельный токен, поэтому не включаем её в строку а матчим её отдельным условием
	SPACE.optional(),
	rule(
		INT,
		DOM_NUMBER_LETTER.optional(),
		rule(
			SLASH,
			INT,
			DOM_NUMBER_LETTER.optional()
		).optional()
	).interpretation(Building.primary)
)

DOM_CORPUS_NUM = rule(
	in_caseless({'корпус', 'корп', 'к'}).optional(),
	DOT.optional(), # точка это отдельный токен, поэтому не включаем её в строку а матчим её отдельным условием
	SPACE.optional(),
	INT.interpretation(Building.korpus)
)

DOM_STROENIE_NUM = rule(
	in_caseless({'строение', 'стр', 'ст', 'с'}).optional(),
	DOT.optional(), # точка это отдельный токен, поэтому не включаем её в строку а матчим её отдельным условием
	SPACE.optional(),
	INT.interpretation(Building.stroenie)
)

DOM_FULL_NUM = rule(
	DOM_PRIMARY_NUM,
	SPACE.optional(),
	DOM_CORPUS_NUM.optional(),
	SPACE.optional(),
	DOM_STROENIE_NUM.optional()
).interpretation(
	Building
)

Room = fact(
	'Room',
	['number', 'type']
)

class Room(Room):
	value = value('number')

###########
#
#   OFIS CPY
#
#############


OFIS_WORDS = or_(
	rule(
		caseless('оф'),
		DOT.optional()
	),
	rule(normalized('офис'))
).interpretation(
	Room.type.const('офис')
)

OFIS_VALUE = ADDR_VALUE.interpretation(
	Room.number
)

OFIS = rule(
	OFIS_WORDS,
	OFIS_VALUE
).interpretation(
	Room
)

###########
#
#   KVARTIRA CPY
#
#############


KVARTIRA_WORDS = or_(
	rule(
		caseless('кв'),
		DOT.optional()
	),
	rule(normalized('квартира'))
).interpretation(
	Room.type.const('квартира')
)

KVARTIRA_VALUE = ADDR_VALUE.interpretation(
	Room.number
)

KVARTIRA = rule(
	KVARTIRA_WORDS,
	KVARTIRA_VALUE
).interpretation(
	Room
)