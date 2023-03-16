import modules.libs.get_from_api as df_preprocessor
import modules.libs.calc as df_calc
import modules.libs.portf as portf_calc
import modules.db_middelware as DB
import pandas as pd
import datetime
import numpy as np

#откат!!!!

def get_data(tickers: list= ["YNDX", "SBER", "VKCO"] , target_risk: float=0.03, target_doh: float=0.0027, portf_count: int=10000):
	df_main = None
	Calc = df_calc.Calc()
	files_lst = []

	for elem in tickers:
		_ = DB.act_get(elem)
		now = datetime.datetime.now()
		if _ == False or _.last != now.strftime("%Y-%m-%d"):
			API = df_preprocessor.API_v2(elem)
			files_lst.append(API.preprocess(API.get_ticker()))
		else:
			files_lst.append(_.cost)


	for name in files_lst:
		df = pd.read_csv(name)
		col_name = name.split("/")[-1].split(".")[-2]
		df = df.rename(columns={"CLOSE": col_name})

	for name in data_list:

		df = df.drop_duplicates(subset=["DATE"],keep="last").reset_index()
		if df_main is None: df_main = df
		else: df_main = pd.concat([df,df_main],sort=False,axis=1)

	df_main = df_main.drop(columns=["index","DATE"]) #main db processing finish
	print(df_main["YNDX"].values)

	mean_matrix, cov_matrix = Calc.auto_calc_spec(df_main)

	print(cov_matrix)
	print("---")
	print(mean_matrix)
	print("---")
	Portf = portf_calc.Portf(mean_matrix, cov_matrix, portf_count)

	risk,doh,portf,count_ = Portf.model()

	'''min_risk = np.argmin(risk)
	max_risk = np.argmax(risk)
	maxSharpKoef = np.argmax(doh/risk)
	r_mean = np.ones(count_)/count_
	risk_mean = Portf.risk(r_mean)
	doh_mean = Portf.profit(r_mean)
	index_target_risk = np.absolute(risk - target_risk).argmin()
	index_target_doh = np.absolute(doh - target_doh).argmin()

	print('---------- Минимальный риск ----------')
	print()
	print("риск = %1.2f%%" % (float(risk[min_risk])*100.))
	print("доходность = %1.2f%%" % (float(doh[min_risk])*100.))
	print()
	print(pd.DataFrame([portf[min_risk]*100],columns=df_main.columns,index=['доли, %']).T)
	print()

	print('---------- Максимальный риск ----------')
	print()
	print("риск = %1.2f%%" % (float(risk[max_risk])*100.))
	print("доходность = %1.2f%%" % (float(doh[max_risk])*100.))
	print()
	print(pd.DataFrame([portf[max_risk]*100],columns=df_main.columns,index=['доли, %']).T)
	print()

	print('---------- Максимальный коэффициент Шарпа [???] ----------')
	print()
	print("риск = %1.2f%%" % (float(risk[maxSharpKoef])*100.))
	print("доходность = %1.2f%%" % (float(doh[maxSharpKoef])*100.))
	print()
	print(pd.DataFrame([portf[maxSharpKoef]*100],columns=df_main.columns,index=['доли, %']).T)
	print()

	print('---------- Средний портфель ----------')
	print()
	print("риск = %1.2f%%" % (float(risk_mean)*100.))
	print("доходность = %1.2f%%" % (float(doh_mean)*100.))
	print()
	print(pd.DataFrame([r_mean*100],columns=df_main.columns,index=['доли, %']).T)
	print()

	print('---------- Целевой риск ----------')
	print()
	print("риск = %1.2f%%" % (float(risk[index_target_risk])*100.))
	print("доходность = %1.2f%%" % (float(doh[index_target_risk])*100.))
	print()
	print(pd.DataFrame([portf[index_target_risk]*100],columns=df_main.columns,index=['доли, %']).T)
	print()

	print('---------- Целевая доходность ----------')
	print()
	print("риск = %1.2f%%" % (float(risk[index_target_doh])*100.))
	print("доходность = %1.2f%%" % (float(doh[index_target_doh])*100.))
	print()
	print(pd.DataFrame([portf[index_target_doh]*100],columns=df_main.columns,index=['доли, %']).T)
	print()'''