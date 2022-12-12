import numpy as np
import pandas as pd
import joblib
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
import seaborn as sns




class GMM():

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

    def createModel(self,ScoreThreshold,nInit=0,nComponents=0,maxIter=100 , OutputFileName=""):
        nComp = 0
        if nComponents > 1:
            nComp = nComponents
        else :
            nComp = 2
        gmm =  GaussianMixture(n_components=nComp, n_init=nInit,max_iter=maxIter)
        y_gmm = gmm.fit_predict(self.data)
        # Get the score for each sample
        score = gmm.score_samples(self.data)
        th=0
        print("ScoreThreshold:",ScoreThreshold)
        if ScoreThreshold != 0:
            th = ScoreThreshold
        else :
            th = self.calcGMMScoreThreshold(score)
        print(th)
        self.dataset['score'] = score
        self.dataset['anomaly_gmm_value'] = self.dataset['score'].apply(lambda x: 1 if x < th else 0)
        # locValue: int = len(self.dataset.columns)
        # self.dataset.insert(loc=locValue, column='KNN OUTPUT', value=labels)
        OutputFile = f"SKlearn/outlierdetection/outputFiels/{OutputFileName}output.csv"
        plt.figure(figsize=(12, 8))
        sns.histplot(self.dataset['score'], bins=100, alpha=0.8)
        # Threshold value
        plt.axvline(x=th, color='orange')
        plt.savefig(r"SKlearn/clustring/images/" + str(OutputFileName))
        plt.clf()
        self.dataset.to_csv(OutputFile, index=False)
        n_components = gmm.n_components
        n_features_in_ = gmm.n_features_in_
        max_iter = gmm.max_iter
        weights_ = gmm.weights_
        means_ = gmm.means_


        return gmm,n_components,n_features_in_,max_iter,weights_,means_,th

    def calcGMMScoreThreshold(self,score):
        q3, q1 = np.percentile(score, [75, 25])
        iqr = q3 - q1
        upper_limit = q3 + (1.5 * iqr)
        lower_limit = q1 - (1.5 * iqr)
        return lower_limit
    def saveModel(self,gmmModel,filename):
        filename = filename
        joblib.dump(gmmModel, filename)

    def CalculateThDistanse(self, distances_mean):
        q3, q1 = np.percentile(distances_mean, [75, 25])
        iqr = q3 - q1
        upper_limit = q3 + (1.5 * iqr)
        return upper_limit