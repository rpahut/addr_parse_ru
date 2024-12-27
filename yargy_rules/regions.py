from value_func import value
from yargy_rules.common import *
from yargy_rules.gender_relation import gender
from yargy.interpretation import attribute
from yargy.pipelines import caseless_pipeline
from addr_parse_ru.constants import DISTRICT_NAMES


Region = fact(
	'Region',
	['name', attribute('type', 'район')]
)


class Region(Region):
	value = value('name')

	def to_string(self):
		if not self.value:
			return ''
		return self.value + ' ' + self.type


############
#
#    OBLAST IMP
#
############


OBLAST_WORDS = or_(
	rule(normalized('область')),
	rule(
		caseless('обл'),
		DOT.optional()
	)
).interpretation(
	Region.type.const('область')
)

OBLAST_NAME = dictionary({
	'амурский',
	'архангельский',
	'астраханский',
	'белгородский',
	'брянский',
	'владимирский',
	'волгоградский',
	'вологодский',
	'воронежский',
	'горьковский',
	'ивановский',
	'ивановский',
	'иркутский',
	'калининградский',
	'калужский',
	'камчатский',
	'кемеровский',
	'кировский',
	'костромской',
	'курганский',
	'курский',
	'ленинградский',
	'липецкий',
	'магаданский',
	'московский',
	'мурманский',
	'нижегородский',
	'новгородский',
	'новосибирский',
	'омский',
	'оренбургский',
	'орловский',
	'пензенский',
	'пермский',
	'псковский',
	'ростовский',
	'рязанский',
	'самарский',
	'саратовский',
	'сахалинский',
	'свердловский',
	'смоленский',
	'тамбовский',
	'тверской',
	'томский',
	'тульский',
	'тюменский',
	'ульяновский',
	'челябинский',
	'читинский',
	'ярославский',
}).interpretation(
	Region.name
)

OBLAST = or_(
	rule(OBLAST_NAME, OBLAST_WORDS),
	rule(OBLAST_WORDS, OBLAST_NAME)
).interpretation(
	Region
)

##########
#
#  RAION IMP
#
###########


MACRORAION_WORDS = or_(
	rule(caseless('р'), DASH, in_caseless({'он', 'н'})),
	rule(normalized('район')),
).interpretation(
	Region.type.const('район')
)

MICRORAION_WORDS = or_(
	rule(caseless('мик'), DASH, in_caseless({'он', 'н'})),
	rule(caseless('м'), DASH, caseless('н')),
	rule(caseless('мрн')),
	rule(caseless('мкр')),
	rule(normalized('микрорайон'))
).interpretation(
	Region.type.const('микрорайон')
)

RAION_WORDS = or_(
	MACRORAION_WORDS,
	MICRORAION_WORDS
)

RAION_MODIFIERS = rule(
	in_caseless({
		'усть',
		'северо',
		'александрово',
		'гаврилово',
	}),
	DASH.optional()
)

RAION_EXACT_NAME = caseless_pipeline(
	DISTRICT_NAMES
).interpretation(
	Region.name
)

RAION_ANUM = rule(
	INT,
	DASH.optional(),
	in_caseless({'й'})
)

RAION_PATTERN = rule(
	or_(
		rule(
			RAION_MODIFIERS.optional(),
			ADJF,
			NOUN.optional()
		),
		rule(
			NOUN
		),
		RAION_ANUM
	)
).interpretation(
	Region.name
)

RAION = rule(
	or_(
		or_(
			rule(RAION_WORDS, RAION_EXACT_NAME),
			rule(RAION_EXACT_NAME, RAION_WORDS),
			RAION_EXACT_NAME
		),
		or_(
			rule(RAION_WORDS, RAION_PATTERN),
			rule(RAION_PATTERN, RAION_WORDS),
		)
	)
).interpretation(
	Region
)