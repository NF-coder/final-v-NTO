import modules.libs.apimoex as apimoex
import requests
import pandas as pd
import datetime

class API_v2:
	def __init__(self, name: str):
		now = datetime.datetime.now()
		year, month, day = now.strftime("%Y-%m-%d").split("-")
		self.start = f"{int(year) - 1}-{month}-{day}"
		self.name = name

	def get_ticker(self):
		with requests.Session() as session:
			data = apimoex.get_market_history(security=self.name, session = session, market ='shares', engine ='stock')
			df = pd.DataFrame(data)
			#df = df.isnull().sum()
			#print(df)
			#df.to_csv("out.csv")
			return df

	def cleanup(self, df):
		df.rename(index=df["TRADEDATE"], inplace=True)
		df = df.drop(columns=["VALUE", "VOLUME", "BOARDID", "TRADEDATE"])
		return df

	def fill(self, df):
		df['CLOSE'] = df['CLOSE'].fillna(method='ffill')
		return df

	def roll(self, df, window:int=5, col: str='CLOSE'):
		df[col].rolling(window).mean()
		return df

	def preprocess(self,df,window:int=5):
		df = self.cleanup(df)
		df = self.fill(df)
		df = self.roll(df,window)
		df = df.truncate(before=self.start)
		df["DATE"] = df.index
		path = f"modules/csv_files/{self.name}.csv"
		df.to_csv(path,index=False)
		return path