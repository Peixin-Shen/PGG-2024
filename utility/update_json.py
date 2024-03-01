import json
import pandas as pd
import math

file_name = '2022-05-02.csv'

df = pd.read_csv("./experi_data/{}".format(file_name))

# 處理 sys_id: 無論 sys 或 user 都會有
sys_id = list(df["pgg.1.player.quit_id"])
print(sys_id)
session_code = df["session.code"][0]

with open('../generated_data/sys_id.json', 'r', encoding='utf-8') as f_read:
	data = json.load(f_read)

	for key, value in data.items():
		if value['ID'] in sys_id:
			print(value['ID'])
			data[key]['Session_code'] = session_code

	with open('../generated_data/sys_id.json', 'w', encoding='utf-8') as f_write:
		json.dump(data, f_write, ensure_ascii=False, indent=4)
		f_write.close()

	f_read.close()

# user_id: 只有 user 有
user_id = list(df["pgg.1.player.pgg_id"])
if df["pgg.1.player.id_treatment"][0] == 'id_user':
	with open('../generated_data/user_id.json','r+', encoding='utf-8') as f2:
		data = json.load(f2)
		for user in user_id:
			try:
				if math.isnan(user):
					pass
			except:
				data[len(data)] = user

		with open('../generated_data/user_id.json','r+', encoding='utf-8') as f3:
			json.dump(data, f3, ensure_ascii=False, indent=4)
			f3.close()
		f2.close()

# 處理隱私資料授權
mpl_agree = df["mpl.1.player.mpl_agree"]
pass_valid = df["mpl.1.player.pass_check"]


if df["session.config.pgg_role"][0] == "A":

	for index, value in enumerate(mpl_agree):
		id_name = str()
		if value == 1 and df["pgg.1.player.id_treatment"][index] == 'id_sys' and pass_valid[index] == 1:
			id_name = sys_id[index]
		elif value == 1 and df["pgg.1.player.id_treatment"][index] == 'id_user' and pass_valid[index] == 1:
			id_name = user_id[index]

		# 同意授權且經過驗證
		if id_name != str():
			# 個別的個資
			with open('../generated_data/info_authorization/{}.json'.format(id_name), 'w', encoding='utf-8') as f1:
				info = dict()
				info["player_id"] = id_name

				for j in range(1, 26):
					ans = list(df["pgg.1.player.q{}".format(j)])[index]
					try:
						if math.isnan(ans):
							ans = ''
					except:
						pass

					info["q" + str(j)] = ans
				json.dump(info, f1, ensure_ascii=False, indent=4)
				f1.close()

			# 授權總表
			with open('../generated_data/id_for_info_authorization.json', 'r+', encoding='utf-8') as f2:
				data = json.load(f2)
				data[str(len(data))] = {
					"name": id_name,
					"usage": 0
				}

			with open('../generated_data/id_for_info_authorization.json','w', encoding='utf-8') as f_write:
				json.dump(data, f_write, ensure_ascii=False, indent=4)
				f_write.close()

elif df["session.config.pgg_role"][0] == "B":
	info_file = df["pgg.1.player.file"]
	for index, value in enumerate(info_file):
		# 授權總表
		with open('../generated_data/id_for_info_authorization.json', 'r+', encoding='utf-8') as f2:
			data = json.load(f2)
			for i, dct in data.items():
				if dct["name"] in value:
					data[i]["usage"] += 1

		with open('../generated_data/id_for_info_authorization.json','w', encoding='utf-8') as f_write:
			json.dump(data, f_write, ensure_ascii=False, indent=4)
			f_write.close()
