import natasha
import natasha.grammars.addr
from yargy import Parser
from yargy.api import or_
from addr_parse_ru.yargy_rules.common import AddrPart
from addr_parse_ru.yargy_rules.regions import OBLAST, RAION
from addr_parse_ru.yargy_rules.okrug import OKRUG
from addr_parse_ru.yargy_rules.settlements import DEREVNYA, SELO, POSELOK, ISLAND
from addr_parse_ru.yargy_rules.streets import STREETS_UNIFIED
from addr_parse_ru.yargy_rules.work_place import BC, ONLY_NAME_BC, FLOOR, PLACE, ONLY_NUMBER_PLACE, SECTOR, ROOM, CABINET, WINDOW, ISU, ONLY_NUMBER_ISU
from addr_parse_ru.yargy_rules.building_values import DOM_FULL_NUM, make_building_tokenizer


reusable_region_parser = None

def yargy_parse_region(text):
	'''
	Извлечь из текста название федерального округа, республики, края, области или автономного округа.
	Функция полагается на наличие соответствующих ключевых слов (республика, обл, фо и прочие).
	В возврате ключевое слово ставится в полной форме перед собственным именем региона.
	'''
	global reusable_region_parser
	if not reusable_region_parser:
		reusable_region_parser = Parser(
			or_(
				natasha.grammars.addr.FED_OKRUG,
				natasha.grammars.addr.RESPUBLIKA,
				natasha.grammars.addr.KRAI,
				OBLAST,
				natasha.grammars.addr.AUTO_OKRUG
			).interpretation(
				AddrPart.value
			).interpretation(
				AddrPart
			)
		)
	
	region_types = ['федеральный округ', 'республика', 'край', 'область', 'автономный округ']
	used_len = 0

	region = ''
	for match in reusable_region_parser.findall(text):
		if not match.fact.value.type is None:
			text = text[0: match.span.start - used_len] + text[match.span.stop - used_len:]
			used_len += match.span.stop - match.span.start
		if match.fact.value.type in region_types:
			region = match.fact.value.type + ' ' + match.fact.value.name
		elif match.fact.value.type is None:
			pass

	return region, text

reusable_okrug_parser = None

def yargy_parse_okrug(text):
	'''
	Извлечь из текста название городского округа.
	Функция полагается на наличие соответствующего ключевого слова.
	В возврате ключевое слово ставится в полной форме после собственного имени округа.
	'''
	global reusable_okrug_parser
	if not reusable_okrug_parser:
		reusable_okrug_parser = Parser(OKRUG)
	
	okrug_types = ['городской округ']
	used_len = 0

	okrug = ''
	for match in reusable_okrug_parser.findall(text):
		if not match.fact.type is None:
			text = text[0: match.span.start - used_len] + text[match.span.stop - used_len:]
			used_len += match.span.stop - match.span.start
		if match.fact.type in okrug_types:
			okrug = match.fact.name + ' ' + match.fact.type
		elif match.fact.type is None:
			pass

	return okrug, text

reusable_district_parser = None

def yargy_parse_district(text):
	'''
	Извлечь из текста название района или микрорайона.
	Функция полагается на наличие соответствующего ключевого слова или наличие собственного имени района во внешнем перечне districts.txt.
	В возврате ключевое слово ставится в полной форме после собственного имени района.
	'''
	global reusable_district_parser
	if not reusable_district_parser:
		reusable_district_parser = Parser(RAION)
	
	district_types = ['район', 'микрорайон']
	used_len = 0

	district = ''
	for match in reusable_district_parser.findall(text):
		if not match.fact.type is None:
			text = text[0: match.span.start - used_len] + text[match.span.stop - used_len:]
			used_len += match.span.stop - match.span.start
		if match.fact.type in district_types:
			district = match.fact.name + ' ' + match.fact.type
		elif match.fact.type is None:
			pass

	return district, text

reusable_settlement_parser = None

def yargy_parse_settlement(text):
	'''
	Извлечь из текста название деревни, села, посёлка или острова.
	Функция полагается на наличие соответствующего ключевого слова.
	В возврате ключевое слово ставится в полной форме перед собственным именем поселения.
	'''
	global reusable_settlement_parser
	if not reusable_settlement_parser:
		reusable_settlement_parser = Parser(
			or_(
				DEREVNYA,
				SELO,
				POSELOK,
				ISLAND
			).interpretation(
				AddrPart.value
			).interpretation(
				AddrPart
			)
		)
	
	settlement_types = ['остров', 'село', 'деревня', 'посёлок']
	used_len = 0

	settlement = ''
	for match in reusable_settlement_parser.findall(text):
		if not match.fact.value.type is None:
			text = text[0: match.span.start - used_len] + text[match.span.stop - used_len:]
			used_len += match.span.stop - match.span.start
		if match.fact.value.type in settlement_types:
			settlement = match.fact.value.type + ' ' + match.fact.value.name
		elif match.fact.value.type is None:
			pass

	return settlement, text

reusable_street_parser = None

def yargy_parse_street(text):
	'''
	Извлечь из текста название улицы, проспекта, проезда, тупика, переулка, площади, шоссе, набережной, бульвара, аллеи, квартала.
	Функция полагается на наличие соответствующего ключевого слова.
	В возврате ключевое слово ставится в полной форме слева перед номером и собственным именем улицы.
	'''
	global reusable_street_parser
	if not reusable_street_parser:
		reusable_street_parser = Parser(STREETS_UNIFIED)
	
	street_types = ['улица', 'проспект', 'проезд', 'тупик', 'переулок', 'площадь', 'шоссе', 'набережная', 'бульвар', 'аллея', 'квартал']
	used_len = 0

	street = ''
	for match in reusable_street_parser.findall(text):
		if not match.fact.value.type is None:
			text = text[0: match.span.start - used_len] + text[match.span.stop - used_len:]
			used_len += match.span.stop - match.span.start
		if match.fact.value.type in street_types:
			street = match.fact.value.to_string()
		elif match.fact.value.type is None:
			pass

	return street, text

reusable_building_parser = None

def yargy_parse_building(text):
	'''
	Извлечь из текста номер дома с опциональной литерой, корпусом, строением.
	Функция способна разобрать номер дома с ключевыми словами или без них, но в последнем случае предполагается минимум посторонних данных в строке.
	В возврате ключевые слова ставятся в полной форме.
	'''
	global reusable_building_parser
	if not reusable_building_parser:
		dom_tokenizer = make_building_tokenizer()
		reusable_building_parser = Parser(DOM_FULL_NUM, dom_tokenizer)
	
	match = reusable_building_parser.find(text)
	dom = ''
	if match:
		dom = match.fact.to_string()
		text = text[0: match.span.start] + text[match.span.stop:]
	return dom, text

reusable_index_parser = None

def yargy_parse_index(text):
	'''
	Извлечь из текста почтовый индекс российского формата.
	'''
	global reusable_index_parser
	if not reusable_index_parser:
		reusable_index_parser = Parser(natasha.grammars.addr.INDEX)

	used_len = 0

	index = ''
	for match in reusable_index_parser.findall(text):
		if not match.fact.type is None:
			text = text[0: match.span.start - used_len] + text[match.span.stop - used_len:]
			used_len += match.span.stop - match.span.start
		if match.fact.type == 'индекс':
			index = match.fact.value
		elif match.fact.type is None:
			pass

	return index, text

reusable_place_parser = None

def yargy_parse_place(text):
	'''
	Извлечь из текста описание рабочего места (бизнес-центра, этажа, номера места, секции, комнаты, кабинета, окна, ряда, бокса, отделения).
	Функция способна разобрать номер дома с ключевыми словами или без них, но в последнем случае предполагается минимум посторонних данных в строке.
	В возврате ключевые слова ставятся в полной форме слева перед значением.
	'''
	global reusable_place_parser
	if not reusable_place_parser:
		reusable_place_parser = Parser(
			or_(
				BC,
				ONLY_NAME_BC,
				FLOOR,
				PLACE,
				ONLY_NUMBER_PLACE,
				SECTOR,
				ROOM,
				CABINET,
				WINDOW,
				ISU,
				ONLY_NUMBER_ISU
			).interpretation(
				AddrPart.value
			).interpretation(
				AddrPart
			)
		)

	workplace_accumulator = []
	workplace_types = ['БЦ', 'АЛЦ', 'окно', 'ряд', 'бокс', 'место', 'кабинет', 'этаж', 'Отделение', 'ВСП/ДО', 'сектор', 'Блок', 'комната']
	used_len = 0

	place = ''
	for match in reusable_place_parser.findall(text):
		if not match.fact.value.type is None:
			text = text[0: match.span.start - used_len] + text[match.span.stop - used_len:]
			used_len += match.span.stop - match.span.start
		if match.fact.value.type in workplace_types:
			workplace_accumulator.append(match.fact.value.type)
			workplace_accumulator.append(match.fact.value.value)
			place = ' '.join(workplace_accumulator)
		elif match.fact.value.type is None:
			pass

	return place, text