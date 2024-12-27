from yargy.tokenizer import QUOTES
from yargy_rules.predicates import *

INT = type('INT')
DOT = eq('.')
SPACE = eq(' ')
ADJF = gram('ADJF')
NOUN = gram('NOUN')
TITLE = is_title()
DASH = eq('-')
SLASH = eq('/')
SEP = in_(r'/\-')
QUOTE = in_(QUOTES)

LETTER = in_caseless(set('абвгдежзийлмнопрстуфхшщэюя'))
LETTER_LATIN = in_caseless(set('qwertyuiopasdfghjlzxcvbnm'))

LETTERS = or_(
	rule(LETTER),
	rule(LETTER_LATIN)
)

ANUM = rule(
	INT,
	DASH.optional(),
	in_caseless({
		'я', 'й', 'е',
		'ое', 'ая', 'ий', 'ой'
	})
)

#########
#
#  Number
#
##########

SIMPLE_NUMBER = rule(
	INT,
	LETTERS.optional()
)

NUMBER_CASES = or_(
	rule(SIMPLE_NUMBER),
	rule(SIMPLE_NUMBER, SEP, SIMPLE_NUMBER),
	rule(SIMPLE_NUMBER, SEP, LETTERS)
)

NUMBER = rule(
	eq('№').optional(),
	NUMBER_CASES
)


#########
#
#  AddrPart
#
##########

AddrPart = fact(
	'AddrPart',
	['value']
)

#work_place_part = fact(
#	'AddrPart',
#	['value']
#)


class work_place_part(AddrPart):
	@property
	def obj(self):
		from natasha import obj

		part = self.value
		return obj.AddrPart(part.value, part.type)