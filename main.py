'''
Демонстрация использования библиотеки
'''
import regex as re
from parsing import parse_address
from postparsing_functions import join_addr_parts

country, region, town, settlement, district, street, building, place, index = parse_address('Московская область, Ленинский городской округ, рп. Боброво, Восточное Бутово м-н, Крымская улица, 1')
exit()

def drop_full_spaces_sents(name):
	name = re.split(r'[\s]\s*', str(name))
	# print(name)
	if name and "" in name:
		name = name.remove("")
	if name and " " in name:
		name = name.remove(" ")
	if not name or len(name) == 0:
		# print("нашлась")
		return None
	return " ".join(name)

if __name__ == '__main__':
	# df = pd.read_excel("sources/addresses.xlsx")
	# df = df['Column1'].to_frame()
	# # df = df.sample(n=10, random_state=42)
	# df['Column1'] = df['Column1'].apply(drop_full_spaces_sents)
	# df = df.dropna()
	# df = df.sample(n=1000, random_state=42)
	# def parsing(s):
	# 	s = str(s)
	# 	return address_parsing(s) #country, region, town, settlement, district, street, building, place, index, result_string =
	# df['country'], df['region'], df['town'], df['settlement'], df['district'], df['street'], df['building'], df['place'], df['index'], df['result_string'] = zip(*df['Column1'].apply(parsing))
	# df.to_excel(r"/Users/a18573916/Desktop/addr_parse/Addr_parse/results/metric1000.xlsx")
	#
#    s = "воронежская область воробьевский район с мужичье ленина 170"
#    country, region, town, settlement, district, street, building, place, index, result_string = address_parsing(s)
#    printer(country, region, town, settlement, district, street, building, place, index)
#    print(result_string)
	print("Путь до файла:")
	filename = input()
	with open("res.csv", "w") as result_file, open(filename, 'r') as f:
		result_file.write("country,region,town,settlement,district,street,building,place,index\n")
		for line in f:
			country, region, town, settlement, district, street, building, place, index = parse_address(line)
			normalized_address = join_addr_parts(country, region, town, settlement, district, street, building, place, index)
			result_file.write(normalized_address + "\n")

