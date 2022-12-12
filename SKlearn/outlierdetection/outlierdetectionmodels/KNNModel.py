import numpy as np
import pandas as pd
import joblib
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt



class KNN():

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

    def createModel(self,distancesThreshold,no_neighbors=5 , OutputFileName=""):
        nbrs = NearestNeighbors(n_neighbors=no_neighbors)
        nbrsModel = nbrs.fit(self.data)
        n_neighbors = nbrs.n_neighbors
        n_features_in_= nbrs.n_features_in_
        n_samples_fit_ = nbrs.n_samples_fit_
        distances, indexes = nbrs.kneighbors(self.data)
        distances_mean = distances.mean(axis=1)
        if distancesThreshold != 0:
            th = distancesThreshold
        else :
            th = self.CalculateThDistanse(distances_mean)
        print(th)
        labels = [1 if i > th else 0 for i in distances_mean]
        locValue: int = len(self.dataset.columns)
        self.dataset.insert(loc=locValue, column='KNN OUTPUT', value=labels)
        OutputFile = f"SKlearn/outlierdetection/outputFiels/{OutputFileName}output.csv"
        plt.figure(figsize=(15, 7))
        plt.plot(distances.mean(axis=1))
        plt.savefig(r"SKlearn/clustring/images/" + str(OutputFileName))
        plt.clf()
        self.dataset.to_csv(OutputFile, index=False)

        return nbrsModel,labels,n_neighbors,n_features_in_,n_samples_fit_,th


    def saveModel(self,nbrsModel,filename):
        filename = filename
        joblib.dump(nbrsModel, filename)

    def CalculateThDistanse(self, distances_mean):
        q3, q1 = np.percentile(distances_mean, [75, 25])
        iqr = q3 - q1
        upper_limit = q3 + (1.5 * iqr)
        return upper_limit