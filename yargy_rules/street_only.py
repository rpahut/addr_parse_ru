from value_func import value
from natasha.grammars.addr import LET, DATE, IMENI, MODIFIER_WORDS
from yargy.interpretation import fact
from yargy import Parser
from yargy import (
    rule,
    or_, and_
)

from yargy.predicates import (
    eq, lte, gte, gram, type, tag,
    length_eq,
    in_, in_caseless, dictionary,
    normalized, caseless,
    is_title
)
from yargy.tokenizer import QUOTES

INT = type('INT')
DOT = eq('.')
ADJF = gram('ADJF')
NOUN = gram('NOUN')
TITLE = is_title()
DASH = eq('-')
SLASH = eq('/')
QUOTE = in_(QUOTES)

ANUM = rule(
    INT,
    DASH.optional(),
    in_caseless({
        'я', 'й', 'е',
        'ое', 'ая', 'ий', 'ой'
    })
)

##########
#
#   ADDR NAME IMP
#
##########


ROD = gram('gent')

SIMPLE = and_(
    or_(
        ADJF,  # Школьная
        and_(NOUN, ROD),  # Ленина, Победы
    )
)

COMPLEX = or_(
    rule(
        and_(ADJF),
        NOUN
    ),
    rule(
        TITLE,
        DASH.optional(),
        TITLE
    ),
)

SPECIAL_CASE_STREET = dictionary({
    'арбат',
    'варварка',
    'мельникайте',
    'каховка',
    'зорге'
})

MAYBE_NAME = or_(
    rule(SIMPLE),
    COMPLEX,
    rule(SPECIAL_CASE_STREET)
)

NAME = or_(
    MAYBE_NAME,
    LET,
    DATE,
    IMENI
)

NAME = rule(
    MODIFIER_WORDS.optional(),
    NAME
)

ADDR_CRF = tag('I').repeatable()

NAME = or_(
    NAME,
    ANUM,
    rule(NAME, ANUM),
    rule(ANUM, NAME),
    rule(INT, DASH.optional(), NAME),
    rule(NAME, DASH, INT),
    ADDR_CRF
)

ADDR_NAME = NAME

########
#
#    STREET NAME IMP W/O STREET_WORDS
#
#########

StreetNameOnly = fact(
    'OnlyStreetName',
    ['name']
)

class StreetNameOnly(StreetNameOnly):
    type = 'улица'
    value = value('name')

STREET_NAME_ONLY = ADDR_NAME.interpretation(
    StreetNameOnly.name
).interpretation(
    StreetNameOnly
)

street_name_only_parser=Parser(STREET_NAME_ONLY)
