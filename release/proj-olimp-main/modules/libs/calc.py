import modules.libs.apimoex as apimoex
import requests
import pandas as pd

class Calc:
    def __init__(self):
        pass

    def change(self,df):
        df = df.pct_change()
        return df.drop (index=df.index [0],axis= 0)

    def mean(self, df):
        col = df.columns
        df = df.mean()
        df.columns = col
        return df

    def cov(self, df):
        return df.cov()

    def auto_calc_mean(self,df):
        return self.mean(self.change(df))

    def auto_calc_cov(self,df):
        return self.cov(self.change(df))

    def del_before_zero(self,df):
        for name, cost in zip(df.index,df.values):
            if cost<=0: df = df.drop(columns=[name])
        return df

    def auto_calc_spec(self, df):
        mean_matrix = self.del_before_zero(self.auto_calc_mean(df))
        cov_matrix = self.auto_calc_cov(df)
        for col in list(set(cov_matrix.columns) - set(mean_matrix.columns)): cov_matrix = cov_matrix.drop(columns=[col])

        return mean_matrix, cov_matrix