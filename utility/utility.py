import random
import json

'''
外生id規則：三個字母加上三個數字，第一個字母是大寫，第二個是英文母音 a e i o u ，第三個是 s z t p 之類的子音，讓名字「可發音」。第四到六碼是「數字」
'''

class ID_generator():
	"""docstring for ID_·generator"""
	def __init__(self):
		self.num_lst = [i for i in range(0, 10)]
		self.vowel_lst = ['a', 'e', 'i', 'o', 'u']
		self.consonant_lst = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
		self.upper_en_lst = [chr(i) for i in range(65, 91)]
		self.var_needed = 200

	def print_lst(self):
		print(self.num_lst)
		print(self.en_lst)

	def generate_id(self):
		lst = list()
		json = dict()

		while len(lst) <= self.var_needed:
			print(len(lst))
			var1 = random.sample(self.upper_en_lst, 1)[0]
			var2 = random.sample(self.vowel_lst, 1)[0]
			var3 = random.sample(self.consonant_lst, 1)[0]
			var4 = random.sample(self.num_lst, 1)[0]
			var5 = random.sample(self.num_lst, 1)[0]
			var6 = random.sample(self.num_lst, 1)[0]

			var = str(var1) + str(var2) + str(var3) + str(var4) + str(var5) + str(var6)

			if var not in lst:
				dct = {
					'Session_code': '',
					'ID': var,
				}
				json[len(lst)] = dct
				lst.append(var)

		return json

	def write_txt(self):
		data = self.generate_id()
		with open('../generated_data/sys_id.json', 'w', encoding='utf-8') as f:
			json.dump(data, f, ensure_ascii=False, indent=4)
		f.close()

a = ID_generator()
a.write_txt()
