import modules.libs.get_from_api as df_preprocessor
import modules.libs.calc as df_calc
import modules.libs.portf as portf_calc
import modules.db_middelware as DB
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

def get_data(outers: list,tickers: list= ["YNDX", "SBER", "VKCO"] , target_risk=None, target_doh=None, portf_count: int=10000):
	df_main = None
	Calc = df_calc.Calc()
	files_lst = []
	course = []

	for elem in tickers:
		_ = DB.act_get(elem)
		now = datetime.datetime.now()
		if _ == False or _.last != now.strftime("%Y-%m-%d"):
			API = df_preprocessor.API_v2(elem)
			df = pd.read_csv(API.preprocess(API.get_ticker()))
			df = df.rename(columns={"CLOSE": elem})
			df = df.drop_duplicates(subset=["DATE"],keep="last").reset_index()
			course.append([df[elem].values[-1], df[elem].values[-1]-df[elem].values[-2]])
			DB.act_upd(elem, df[elem].values)
			files_lst.append(df.copy(deep=True))
		else:
			print("in cahe", elem)
			df = pd.DataFrame({elem:list(map(float,_.cost.split()))})
			course.append([df[elem].values[-1], df[elem].values[-1]-df[elem].values[-2]])
			files_lst.append(df.copy(deep=True))

	for df in files_lst:
		if df_main is None: df_main = df
		else: df_main = pd.concat([df,df_main],sort=False,axis=1)

	try: df_main = df_main.drop(columns=["index","DATE"]) #main db processing finish
	except: pass

	mean_matrix, cov_matrix = Calc.auto_calc_spec(df_main)
	Portf = portf_calc.Portf(mean_matrix, cov_matrix, portf_count)
	risk,doh,portf,count_ = Portf.model()

	min_risk = np.argmin(risk)
	max_risk = np.argmax(risk)
	maxSharpKoef = np.argmax(doh/risk)
	r_mean = np.ones(count_)/count_
	risk_mean = Portf.risk(r_mean)
	doh_mean = Portf.profit(r_mean)
	if target_risk is not None: index_target_risk = np.absolute(risk - target_risk).argmin()
	if target_doh is not None:index_target_doh = np.absolute(doh - target_doh).argmin()

	return_dict = {}

	if target_risk is not None:
		data = {
			"риск": "%1.2f%%" % (float(risk[index_target_risk])*100.),
			"доходность": "%1.2f%%" % (float(doh[index_target_risk])*100.),
			"доли": pd.DataFrame([portf[index_target_risk]*100],columns=df_main.columns,index=['доли, %']).T
		}
		return_dict["Целевой риск"] = data

	if target_doh is not None:
		data = {
			"риск": "%1.2f%%" % (float(risk[index_target_doh])*100.),
			"доходность": "%1.2f%%" % (float(doh[index_target_doh])*100.),
			"доли": pd.DataFrame([portf[index_target_doh]*100],columns=df_main.columns,index=['доли, %']).T
		}
		return_dict["Целевой доход"] = data

	if "Средний портфель" in outers:
		data = {
			"риск": "%1.2f%%" % (float(risk_mean)*100.),
			"доходность": "%1.2f%%" % (float(doh_mean)*100.),
			"доли": pd.DataFrame([r_mean*100],columns=df_main.columns,index=['доли, %']).T
		}

		return_dict["Средний портфель"] = data

	if "Портфель с максимальным коэффициентом Шарпа" in outers:
		data = {
			"риск": "%1.2f%%" % (float(risk[maxSharpKoef])*100.),
			"доходность": "%1.2f%%" % (float(doh[maxSharpKoef])*100.),
			"доли": pd.DataFrame([portf[maxSharpKoef]*100],columns=df_main.columns,index=['доли, %']).T
		}

		return_dict["Портфель с максимальным коэффициентом Шарпа"] = data

	if "Портфель с минимальным риском" in outers:
		data = {
			"риск": "%1.2f%%" % (float(risk[min_risk])*100.),
			"доходность": "%1.2f%%" % (float(doh[min_risk])*100.),
			"доли": pd.DataFrame([portf[min_risk]*100],columns=df_main.columns,index=['доли, %']).T
		}

		return_dict["Портфель с минимальным риском"] = data

	if "Портфель с максимальным риском" in outers:
		data = {
			"риск": "%1.2f%%" % (float(risk[max_risk])*100.),
			"доходность": "%1.2f%%" % (float(doh[max_risk])*100.),
			"доли": pd.DataFrame([portf[max_risk]*100],columns=df_main.columns,index=['доли, %']).T
		}

		return_dict["Портфель с максимальным риском"] = data

	if "Облако портфелей" in outers:
		plt.Figure(figsize=(10,8))
		plt.scatter(risk*100,doh*100,c='y',marker='.')
		plt.xlabel('риск, %')
		plt.ylabel('доходность, %')
		plt.title("Облако портфелей")
		
		plt.scatter([(risk[min_risk])*100],[(doh[min_risk])*100],c='r',marker='*',label='минимальный риск')
		plt.scatter([risk[maxSharpKoef]*100],[doh[maxSharpKoef]*100],c='g',marker='o',label='максимальный коэф-т Шарпа')
		plt.scatter([risk_mean*100],[doh_mean*100],c='b',marker='x',label='усредненный портфель')
		
		plt.legend()

		path = "imgs/plot.jpg"
		plt.savefig(path)

		return_dict["Облако портфелей"] = path

	if "Текущий курс" in outers:
		data = {}
		for i in range(len(tickers)):
			elem = tickers[i]
			data[elem] = [course[i][0],course[i][1]]

		return_dict["Текущий курс"] = data

	if "Плавающее среднее" in outers:
		data = {}
		for i in range(len(tickers)):
			elem = tickers[i]
			print(files_lst, elem)
			_ = files_lst[elem].values
			print(_)
			data[elem] = pd.DataFrame({elem:_}).rolling(5).mean()

		return_dict["Плавающее среднее"] = data

	return return_dict
