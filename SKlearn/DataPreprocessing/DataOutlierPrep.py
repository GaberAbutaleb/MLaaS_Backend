import numpy as np
import pandas as pd
from numpy import mean
from numpy import std
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest


class OutlierPrep:
    def __init__(self, df):
        self.df = df

    def stdMethod(self, column):
        # calculate summary statistics
        data_mean, data_std = mean(column), std(column)
        # identify outliers
        cut_off = data_std * 3
        lower, upper = data_mean - cut_off, data_mean + cut_off
        outliers = [x for x in column if (x < lower) or (x > upper)]
        return outliers

    def iqrMethod(self, column):
        # calculate interquartile range
        q25, q75 = np.percentile(column, 25), np.percentile(column, 75)
        iqr = q75 - q25
        # calculate the outlier cutoff
        cut_off = iqr * 1.5
        lower, upper = q25 - cut_off, q75 + cut_off
        # identify outliers
        outliers = [x for x in column if x < lower or x > upper]
        return outliers

    def zScoreMethod(self, data, threshold=3):
        outliers = list()
        thres = threshold
        mean = np.mean(data)
        std = np.std(data)
        # print(mean, std)
        for i in data:
            z_score = (i - mean) / std
            if (np.abs(z_score) > thres):
                outliers.append(i)
        return outliers

    def IsolationForestMethod(self):
        random_state = np.random.RandomState(42)
        model = IsolationForest(n_estimators=100, max_samples='auto', contamination=float(0.1),
                                random_state=random_state)
        model.fit(self.df)
        self.df['anomaly_score'] = model.predict(self.df)
        return self.df[self.df['anomaly_score'] == -1]

    def boxplot(self, column):
        sns.boxplot(data=self.df, x=column.values)
        plt.title(f"Boxplot of Credit Scoring ")
        plt.show()

    def handleOutlieriesQBFC(self, column, min, max):
        #         print("handleOutlieriesQBFC")
        # Computing 10th, 90th percentiles and replacing the outliers
        tenth_percentile = np.percentile(column, min)
        ninetieth_percentile = np.percentile(column, max)
        print(tenth_percentile, ninetieth_percentile)
        b = np.where(column < tenth_percentile, tenth_percentile, column)
        b = np.where(column > ninetieth_percentile, ninetieth_percentile, b)
        # print("Sample:", sample)
        return b

    def handleOutlieriesMedianMean(self, column, columnOutliers=list(), method="median"):
        #         print("handleOutlieriesMedianMean")
        outliers = columnOutliers
        value = 0
        if method == 'median':
            value = self.df[column].median()
        elif method == 'mode':
            value = self.df[column].mode()
        else:
            value = self.df[column].mean()
        for i in outliers:
            self.df[column] = np.where(np.array(self.df[column]) == i, value, self.df[column])
        return self.df[column]

    def handleOutlieriesLogTransform(self, column):
        self.df[column] = self.df[column].map(lambda i: np.log(i) if i > 0 else 0)
        return self.df[column]

    # HandlingOutlierMethod [median,mean,mode,qbfc,remove,logtransform]
    #  detectionMethod  [iqrMethod,zscoreMethod ,stdMethod]
    def handleAllOutliers(self,data=pd.DataFrame(), HandlingMethod="median", detectionMethod="iqrMethod"):

        print("handleAllOutliers Start")
        numerical_Columns = list()
        categorical_Columns = list()
        for column, coltype in data.dtypes.iteritems():
            if coltype != "object":
                numerical_Columns.append(column)
            else:
                categorical_Columns.append(column)
        # print(numerical_Columns)
        # print(categorical_Columns)
        outlierPrepobj = OutlierPrep(data)
        for column in numerical_Columns:
            outliers = self.detectOutlierMethod(detectionMethod, data[column], outlierPrepobj)
            if len(outliers) != 0:
                print("outliers Column: ", column)
                data[column] = self.HandlingOutlierMethod(data, HandlingMethod, column, outlierPrepobj, outliers)
                for i in range(0):
                    outliers = self.detectOutlierMethod(detectionMethod, data[column], outlierPrepobj)
                    print(column, outliers)
                    if len(outliers) != 0:
                        data[column] = self.HandlingOutlierMethod(data, HandlingMethod, column, outlierPrepobj, outliers)
        #                     outliers = detectOutlierMethod(detectionMethod,data[column],outlierPrepobj)

        print("________________________________________________")
        for column in numerical_Columns:
            outliers = self.detectOutlierMethod(detectionMethod, data[column], outlierPrepobj)
            print(column, outliers)
        print("handleAllOutliers end")
        return data

    def detectOutlierMethod(self,detectionMethod, column, outlierPrepobj):
        outliers = list()
        if detectionMethod == "iqrMethod":
            outliers = outlierPrepobj.iqrMethod(column)
        elif detectionMethod == "zscoreMethod":
            outliers = outlierPrepobj.zScoreMethod(column, threshold=3)
        elif detectionMethod == "stdMethod":
            outliers = outlierPrepobj.stdMethod(column)
        return outliers

    # HandlingOutlierMethod [median,mean,mode,qbfc,remove,logtransform]
    def HandlingOutlierMethod(self,data, HandlingMethod, column, outlierPrepobj, outliers):

        outliers = outliers
        if HandlingMethod == "median":
            data[column] = outlierPrepobj.handleOutlieriesMedianMean(column, columnOutliers=outliers, method="median")
        elif HandlingMethod == "mean":
            data[column] = outlierPrepobj.handleOutlieriesMedianMean(column, columnOutliers=outliers, method="mean")
        elif HandlingMethod == "mode":
            data[column] = outlierPrepobj.handleOutlieriesMedianMean(column, columnOutliers=outliers, method="mode")
        elif HandlingMethod == "qbfc":
            data[column] = outlierPrepobj.handleOutlieriesQBFC(data[column], 10, 90)
        #     elif HandlingMethod == "remove":
        #         data[column]=outlierPrepobj.handleOutlieriesMedianMean( column,columnOutliers=outliers)
        #     elif HandlingMethod == "logtransform":
        #         data[column]=outlierPrepobj.handleOutlieriesMedianMean( column,columnOutliers=outliers)
        return data[column]