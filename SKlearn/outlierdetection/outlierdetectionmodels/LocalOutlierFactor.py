import numpy as np
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
import joblib


class LOF():

    def __init__(self, filePath=None, noOfRows=0,noOfColumns=0):
        if filePath:
            print("file is readed")
            self.dataset = pd.read_csv(filePath)
            if noOfRows == 0 and noOfColumns == 0:
                self.data = self.dataset.iloc[:, :].values
            elif noOfRows != 0 and noOfColumns == 0:
                self.data = self.dataset.iloc[:noOfRows, :].values
            elif noOfRows == 0 and noOfColumns != 0:
                self.data = self.dataset.iloc[:, :noOfColumns].values
            else:
                self.data = self.dataset.iloc[:noOfRows, :noOfColumns].values
            print(self.data.shape)

    def createModel(self,no_neighbors=5, OutputFileName=""):
        lof_outlier = LocalOutlierFactor(n_neighbors=no_neighbors, novelty=False)
        prediction_outlier = lof_outlier.fit_predict(self.data)
        labels = [1 if i == -1 else 0 for i in prediction_outlier]
        locValue: int = len(self.dataset.columns)
        self.dataset.insert(loc=locValue, column='LOF output', value=labels)
        OutputFile = f"SKlearn/outlierdetection/outputFiels/{OutputFileName}output.csv"
        self.dataset.to_csv(OutputFile, index=False)
        leaf_size=lof_outlier.leaf_size
        n_features_in_= lof_outlier.n_features_in_
        n_neighbors= lof_outlier.n_neighbors
        n_samples_fit_= lof_outlier.n_samples_fit_

        return lof_outlier,labels,leaf_size,n_features_in_,n_neighbors,n_samples_fit_


    def saveModel(self,LOFModel,filename):
        filename = filename
        joblib.dump(LOFModel, filename)