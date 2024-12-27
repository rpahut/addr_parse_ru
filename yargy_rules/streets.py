from yargy.pipelines import caseless_pipeline
from yargy_rules.settlements import Settlement
from yargy_rules.gender_relation import gender
from yargy_rules.common import *
from value_func import value
from yargy_rules.addr_name import ADDR_NAME
from yargy.interpretation import attribute


Street = fact(
	'Street',
	[attribute('numeral', None), 'name', 'type']
)


class Street(Street):
	value = value('name')

	def to_string(self):
		ret = None
		if self.type:
			ret = self.type
			if self.numeral:
				ret = self.numeral + ' ' + ret
			if self.name:
				ret += ' ' + self.name
		return ret


########
#
#    STREET IMP
#
#########

# в отличие от ANUM допускает только склонения совпадающие с "улица"
STREET_NUMERAL = rule(
	INT,
	DASH.optional(),
	eq('я')
).interpretation(Street.numeral)

STREET_WORDS = or_(
	rule(normalized('улица')),
	rule(
		caseless('ул'),
		DOT.optional()
	)
).interpretation(
	Street.type.const('улица')
).match(gender)

STREET_NAME_SPECIAL = caseless_pipeline(
	['набережная']
)

STREET_NAME = or_(
	rule(ADJF)
		.interpretation(Street.name)
		.match(gender),
	rule(ADDR_NAME)
		.interpretation(Street.name),
	STREET_NAME_SPECIAL.interpretation(Street.name),
)

STREET = rule(
	STREET_NUMERAL.optional(),
	or_(
		rule(STREET_WORDS, STREET_NAME),
		rule(STREET_NAME, STREET_WORDS)
	)
).interpretation(
	Street
)

##########
#
#    PROSPEKT IMP
#
##########

PROSPEKT_WORDS = or_(
	rule(
		in_caseless({'пр', 'просп'}),
		DOT.optional()
	),
	rule(
		caseless('пр'),
		'-',
		in_caseless({'кт', 'т'}),
		DOT.optional()
	),
	rule(normalized('проспект'))
).interpretation(
	Street.type.const('проспект')
).match(gender)

PROSPEKT_NAME = or_(rule(ADJF).interpretation(
	Street.name).match(gender),
					rule(ADDR_NAME).interpretation(
						Street.name)
					)

PROSPEKT = or_(
	rule(PROSPEKT_WORDS, PROSPEKT_NAME),
	rule(PROSPEKT_NAME, PROSPEKT_WORDS)
).interpretation(
	Street
)

############
#
#    PROEZD IMP
#
#############


PROEZD_WORDS = or_(
	rule(caseless('пр'), DOT.optional()),
	rule(
		caseless('пр'),
		'-',
		in_caseless({'зд', 'д'}),
		DOT.optional()
	),
	rule(normalized('проезд'))
).interpretation(
	Street.type.const('проезд')
).match(gender)

PROEZD_NAME = or_(rule(ADJF).interpretation(
	Street.name).match(gender),
				  rule(ADDR_NAME).interpretation(
					  Street.name)
				  )

PROEZD = or_(
	rule(PROEZD_WORDS, PROEZD_NAME),
	rule(PROEZD_NAME, PROEZD_WORDS)
).interpretation(
	Street
)

############
#
#    TUPIK IMP
#
#############


TUPIK_WORDS = or_(
	rule(caseless('туп'), DOT.optional()),
	rule(normalized('тупик'))
).interpretation(
	Street.type.const('тупик')
).match(gender)

TUPIK_NAME = or_(
	rule(ADJF).interpretation(
		Street.name).match(gender),
	rule(ADDR_NAME).interpretation(
		Street.name)
	)

TUPIK = or_(
	rule(TUPIK_WORDS, TUPIK_NAME),
	rule(TUPIK_NAME, TUPIK_WORDS)
).interpretation(
	Street
)

###########
#
#   PEREULOK IMP
#
##############


PEREULOK_WORDS = or_(
	rule(
		caseless('п'),
		DOT
	),
	rule(
		caseless('пер'),
		DOT.optional()
	),
	rule(normalized('переулок'))
).interpretation(
	Street.type.const('переулок')
).match(gender)

PEREULOK_NAME = or_(rule(ADJF).interpretation(
	Street.name).match(gender),
					rule(ADDR_NAME).interpretation(
						Street.name)
					)

PEREULOK = or_(
	rule(PEREULOK_WORDS, PEREULOK_NAME),
	rule(PEREULOK_NAME, PEREULOK_WORDS)
).interpretation(
	Street
)

########
#
#  PLOSHAD IMP
#
##########


PLOSHAD_WORDS = or_(
	rule(
		caseless('пл'),
		DOT.optional()
	),
	rule(normalized('площадь'))
).interpretation(
	Street.type.const('площадь')
).match(gender)

PLOSHAD_NAME = or_(rule(ADJF).interpretation(
	Street.name).match(gender),
				   rule(ADDR_NAME).interpretation(
					   Street.name)
				   )

PLOSHAD = or_(
	rule(PLOSHAD_WORDS, PLOSHAD_NAME),
	rule(PLOSHAD_NAME, PLOSHAD_WORDS)
).interpretation(
	Street
)

########
#
#  ADDR VALUE IMP
#
##########

ADDR_VALUE_LETTER = or_(
	rule(LETTER),
	rule(QUOTE, LETTER, QUOTE)
)

VALUE = rule(
	INT,
	ADDR_VALUE_LETTER.optional()
)

SEP = in_(r'/\-')

VALUE = or_(
	rule(VALUE),
	rule(VALUE, SEP, VALUE),
	rule(VALUE, SEP, ADDR_VALUE_LETTER),
)

ADDR_VALUE = rule(
	eq('№').optional(),
	VALUE
)

############
#
#   SHOSSE IMP
#
###########

SHOSSE_WORDS = or_(
	rule(
		caseless('ш'),
		DOT.optional()
	),
	rule(normalized('шоссе'))
).interpretation(
	Street.type.const('шоссе')
).match(gender)

SHOSSE_NAME = or_(rule(ADJF).interpretation(
	Street.name).match(gender),
				  rule(ADDR_NAME).interpretation(
					  Street.name)
				  )

SHOSSE = or_(
	rule(SHOSSE_NAME, SHOSSE_WORDS),
	rule(SHOSSE_WORDS, SHOSSE_NAME)
).interpretation(
	Street
)

########
#
#  NABEREG IMP
#
##########


NABEREG_WORDS = or_(
	rule(
		caseless('наб'),
		DOT.optional()
	),
	rule(normalized('набережная'))
).interpretation(
	Street.type.const('набережная')
).match(gender)

NABEREG_NAME = or_(rule(ADJF).interpretation(
	Street.name).match(gender),
				   rule(ADDR_NAME).interpretation(
					   Street.name)
				   )

NABEREG = or_(
	rule(NABEREG_WORDS, NABEREG_NAME),
	rule(NABEREG_NAME, NABEREG_WORDS)
).interpretation(
	Street
)

########
#
#  BULVAR IMP
#
##########


BULVAR_WORDS = or_(
	rule(
		caseless('б'),
		'-',
		caseless('р'),
		DOT.optional()
	),
	rule(
		caseless('б'),
		DOT
	),
	rule(
		caseless('бул'),
		DOT.optional()
	),
	rule(normalized('бульвар'))
).interpretation(
	Street.type.const('бульвар')
).match(gender)

BULVAR_NAME = or_(rule(ADJF).interpretation(
	Street.name).match(gender),
				  rule(ADDR_NAME).interpretation(
					  Street.name)
				  )

BULVAR = or_(
	rule(BULVAR_WORDS, BULVAR_NAME),
	rule(BULVAR_NAME, BULVAR_WORDS)
).interpretation(
	Street
)

########
#
#  ALLEYA IMP
#
##########


ALLEYA_WORDS = or_(
	rule(
		caseless('ал'),
		DOT.optional()
	),
	rule(normalized('аллея'))
).interpretation(
	Street.type.const('аллея')
).match(gender)

ALLEYA_NAME = or_(
	rule(ADJF).interpretation(
		Street.name
	).match(gender),
	rule(ADDR_NAME).interpretation(
		Street.name)
	)

ALLEYA = or_(
	rule(ALLEYA_WORDS, ALLEYA_NAME),
	rule(ALLEYA_NAME, ALLEYA_WORDS)
).interpretation(
	Street
)


########
#
#  KVARTAL IMP
#
##########

KVARTAL_WORDS = or_(
	rule(
		caseless('кв'),
		DASH,
		caseless('л'),
	),
	rule(normalized('квартал'))
).interpretation(
	Street.type.const('квартал')
).match(gender)

KVARTAL_ANUM = rule(
	INT,
	DASH.optional(),
	in_caseless({'й'})
)

KVARTAL_NUMLETTER = rule(
	INT,
	LETTER
)

KVARTAL_NAME = rule(
	or_(
		rule(
			ADDR_NAME,
			KVARTAL_NUMLETTER.optional(),
			KVARTAL_ANUM.optional()
		),
		rule(
			NOUN,
			KVARTAL_NUMLETTER.optional(),
			KVARTAL_ANUM.optional()
		),
		KVARTAL_NUMLETTER
	)
).interpretation(
	Street.name
)

KVARTAL = or_(
	rule(KVARTAL_WORDS, KVARTAL_NAME),
	rule(KVARTAL_NAME, KVARTAL_WORDS)
).interpretation(
	Street
)


########
#
#  STREETS_UNIFIED IMP
#
##########

STREETS_UNIFIED = or_(
	STREET,
	PROSPEKT,
	PROEZD,
	TUPIK,
	PEREULOK,
	PLOSHAD,
	SHOSSE,
	NABEREG,
	BULVAR,
	ALLEYA,
	KVARTAL
).interpretation(
	AddrPart.value
).interpretation(
	AddrPart
)