from value_func import value
from yargy_rules.common import *
from yargy.interpretation import attribute
from yargy.pipelines import caseless_pipeline
from addr_parse_ru.constants import SETTLEMENT_NAMES


Okrug = fact(
	'Okrug',
	['name', attribute('type', 'городской округ')]
)


class Okrug(Okrug):
	value = value('name')

	def to_string(self):
		if not self.value:
			return ''
		return self.value + ' ' + self.type

##########
#
#  OKRUG IMP
#
###########


OKRUG_WORDS = or_(
	rule(caseless('г'), SPACE.optional(), DOT.optional(), caseless('о'), SPACE.optional(), DOT.optional()),
	rule(normalized('городской округ')),
).interpretation(
	Okrug.type.const('городской округ')
)

OKRUG_EXACT_NAME = caseless_pipeline(
	SETTLEMENT_NAMES
).interpretation(
	Okrug.name
)

OKRUG_PATTERN = rule(
	or_(
		rule(
			ADJF,
			NOUN.optional()
		),
		rule(
			NOUN
		)
	)
).interpretation(
	Okrug.name
)

OKRUG = rule(
	or_(
        rule(OKRUG_WORDS, OKRUG_EXACT_NAME),
        rule(OKRUG_EXACT_NAME, OKRUG_WORDS),
        rule(OKRUG_WORDS, OKRUG_PATTERN),
        rule(OKRUG_PATTERN, OKRUG_WORDS)
	)
).interpretation(
	Okrug
)