import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
import math


class DataCleaning:

    def fill_missing_value(self, Data, missing_values, strategy, fill_value):
        if strategy == 'constant':
            imp = SimpleImputer(missing_values=missing_values, fill_value=fill_value, strategy=strategy)
        else:
            imp = SimpleImputer(missing_values=missing_values, strategy=strategy)
        imp = imp.fit(Data)
        modified_data = imp.transform(Data)
        return modified_data

    def data_exploration(self, df):
        df.info()
        print("__________________________________________________________")
        nullHeatMapImage = sns.heatmap(df.isnull(), cbar=False)
        print(df.isnull().sum())
        print(nullHeatMapImage.get_figure())
        print("__________________________________________________________")

    # Deleting the column with missing data
    def dropNullcolumn(self, df, columnName):
        df.drop(columnName, axis=1, inplace=True)
        return df

    # Drop List of null columns from df
    def dropListOfNullColumns(self, df, DataCleaningobj):
        dropColumnsList = [i for i in df.columns if df[i].isnull().any()]
        newdf = pd.DataFrame()
        for columnName in dropColumnsList:
            newdf = DataCleaningobj.dropNullcolumn(df, columnName)
        return newdf

    # Deleting the row with missing data
    def dropNullrows(self, df):
        updated_df = df.dropna(axis=0)
        return updated_df

    # Keep only the rows with at least No thresh non-NA values:
    def KeepRowsWithnonNA(self, df, threshold):
        updated_df = df.dropna(thresh=threshold)
        return updated_df

    # Filling the Missing Values – Imputation
    def imputationMissingValues(self, df, columnName, strategyName="mean"):
        updated_df = df
        if (strategyName == "mean"):
            updated_df[columnName] = updated_df[columnName].fillna(updated_df[columnName].mean())
            return updated_df
        elif (strategyName == "median"):
            updated_df[columnName] = updated_df[columnName].fillna(updated_df[columnName].median())
            return updated_df[columnName]
        elif (strategyName == "mode"):
            updated_df[columnName] = updated_df[columnName].fillna(updated_df[columnName].mode())
            return updated_df[columnName]
        elif (strategyName == "most_frequent"):
            imp = SimpleImputer(missing_values=np.nan, strategy=strategyName)
            updated_df[columnName] = imp.fit_transform(updated_df[columnName].to_numpy().reshape(-1, 1))
            return updated_df[columnName]

    #  Filling with a Regression Model
    def fillByRegressionModel(self, orginaldf, regressionTargetColumn):
        print("fillByRegressionModel")
        df = orginaldf
        lr = LinearRegression()
        testdf = df[df[regressionTargetColumn].isnull() == True]
        traindf = df[df[regressionTargetColumn].isnull() == False]
        y = traindf[regressionTargetColumn]
        traindf.drop(regressionTargetColumn, axis=1, inplace=True)
        lr.fit(traindf, y)
        for i in df[df[regressionTargetColumn].isnull() == True].index:
            df[regressionTargetColumn][i] = math.floor(
                lr.predict(np.array(df.drop([regressionTargetColumn], axis=1).loc[i]).reshape(1, -1)))
        return df

    # HandlingOutlierMethod [dropNullcolumns,dropListOfNullColumns,dropNullrows,KeepRowsWithnonNA,
    # mean,median,most_frequent,fillByRegressionModel]
    # def handleAllMissingValues(data = pd.DataFrame(),HandlingMethod ="median"):
    def HandlingMissingValuesMethod(self,originalDataFrame, HandlingMethod="", columnList=[], threshold=4,
                                    regressionTargetColumn=""):
        print("HandlingMissingValuesMethod Start")
        DataCleaningobj = DataCleaning()
        dataFrame = pd.DataFrame()
        result = pd.DataFrame()

        if columnList:
            print("columnList",columnList)
            dataFrame = originalDataFrame[columnList]
        else:
            dataFrame = originalDataFrame
        #     print("dataFrame")
        #     print(dataFrame)
        if HandlingMethod == "median":
            for columnName in dataFrame.columns:
                dataFrame[columnName] = self.HandlingColumn(dataFrame, columnName, DataCleaningobj, strategyName="median")
        #             print(dataFrame[columnName])
        elif HandlingMethod == "mean":
            for columnName in dataFrame.columns:
                dataFrame[columnName] = self.HandlingColumn(dataFrame, columnName, DataCleaningobj, strategyName="mean")
        elif HandlingMethod == "mode":
            for columnName in dataFrame.columns:
                dataFrame[columnName] = self.HandlingColumn(dataFrame, columnName, DataCleaningobj, strategyName="mode")
        elif HandlingMethod == "dropListOfNullColumns":
            dataFrame = DataCleaningobj.dropListOfNullColumns(dataFrame, DataCleaningobj)
        elif HandlingMethod == "dropNullrows":
            dataFrame = DataCleaningobj.dropNullrows(dataFrame)
        elif HandlingMethod == "KeepRowsWithnonNA":
            dataFrame = DataCleaningobj.KeepRowsWithnonNA(dataFrame, threshold)
        elif HandlingMethod == "fillByRegressionModel":
            numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
            dataFrame = dataFrame.select_dtypes(include=numerics)
            dataFrame = DataCleaningobj.fillByRegressionModel(dataFrame, regressionTargetColumn)

        if columnList:
            #         dataFrame =dataFrame[columnList]
            print("columnListAgain")
            originalDataFrame = originalDataFrame.drop(columnList, axis=1)
            result = pd.concat([originalDataFrame, dataFrame], axis=1)
        else:
            result = dataFrame
        print("HandlingMissingValuesMethod End")
        return result

    def HandlingColumn(self,dataFrame, colName, DataCleaningobj, strategyName="median"):
        if dataFrame.dtypes[colName] != "object":
            # print(colName, " is numerical")
            dataFrame[colName] = DataCleaningobj.imputationMissingValues(dataFrame, colName, strategyName="median")
        else:
            # print(colName, " is categorical")
            dataFrame[colName] = DataCleaningobj.imputationMissingValues(dataFrame, colName,
                                                                         strategyName="most_frequent")

        return dataFrame[colName]
