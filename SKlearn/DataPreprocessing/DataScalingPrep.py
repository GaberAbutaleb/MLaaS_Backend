import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MaxAbsScaler


class DataScaling():

    # MinMaxScaler (Normalization)
    def ScaleByMinMaxScaler(self, df, columnsList):
        scaler = MinMaxScaler()
        for column in columnsList:
            if df[column].dtypes != "object":
                df[[column]] = scaler.fit_transform(df[[column]])
        return df

    # Standard Scaler (Standardization)
    def ScaleByStandardScaler(self, df, columnsList):
        scaler = StandardScaler(copy=True, with_mean=True, with_std=True)
        for column in columnsList:
            if df[column].dtypes != "object":
                df[[column]] = scaler.fit_transform(df[[column]])
        return df

    # MaxAbsScaler
    def ScaleByMaxAbsScalerScaler(self, df, columnsList):
        scaler = MaxAbsScaler(copy=True)
        for column in columnsList:
            if df[column].dtypes != "object":
                df[[column]] = scaler.fit_transform(df[[column]])
        return df
    def HandlingScale(self,df=pd.DataFrame(),columnsList=[],scaleMethod="StandardScaler"):
        if not columnsList:
            columnsList = df.columns
        if(scaleMethod == "StandardScaler"):
            df = self.ScaleByStandardScaler(df,columnsList)
            return df
        elif(scaleMethod == "MaxAbsScaler"):
            df = self.ScaleByMaxAbsScalerScaler(df,columnsList)
            return df
        elif(scaleMethod == "MinMaxScaler"):
            df = self.ScaleByMinMaxScaler(df,columnsList)
            return df