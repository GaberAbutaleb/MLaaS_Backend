from typing import List

import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from kneed import  KneeLocator
import joblib


class Kmeans():

    def __init__(self, filePath=None, noOfRows=0,noOfColumns=0):
        if filePath:
            print("file is readed")
            dataset = pd.read_csv(filePath)
            if noOfRows == 0 and noOfColumns == 0:
                self.data = dataset.iloc[:, :].values
            elif noOfRows != 0 and noOfColumns == 0:
                self.data = dataset.iloc[:noOfRows, :].values
            elif noOfRows == 0 and noOfColumns != 0:
                self.data = dataset.iloc[:, :noOfColumns].values
            else:
                self.data = dataset.iloc[:noOfRows, :noOfColumns].values
            #print(self.data )
            print(self.data.shape)

    def createmodel(self,k=0,method="elbow"):

        if k == 0 :
            modelK= self.bestK(method)
        else:
            modelK = k
        kmeans = KMeans(n_clusters=modelK, init='k-means++', max_iter = 300)
        y_kmeans = kmeans.fit_predict(self.data)
        numberOfK = modelK
        print("numberOfK",modelK)
        return kmeans,y_kmeans , numberOfK
    #def readFile(self,filePath):


    def bestK(self, method ):
        #print("bestK ")
        #print(self.data.shape)
        data_frame = self.data
        range_n_clusters = [2, 3, 4, 5, 6, 7, 8]
        silhouette_avg = []
        wcss = []
        for num_clusters in range_n_clusters:
            # initialise kmeans
            kmeans = KMeans(n_clusters=num_clusters, init='k-means++')
            kmeans.fit(data_frame)
            cluster_labels = kmeans.labels_
            if method == "silhouette":
                silhouette_avg.append(silhouette_score(data_frame, cluster_labels))
            else:
                wcss.append(kmeans.inertia_)
        if method == "silhouette":
            K = range_n_clusters[silhouette_avg.index(max(silhouette_avg))]
            print("The best k from silhouette",K )
            return K
        else:
            kn = KneeLocator(range_n_clusters,wcss,S=1.0, curve='convex', direction='decreasing', interp_method='interp1d' )
            print("The best k from elbow",kn.elbow)
            plt.plot(range_n_clusters, wcss)
            plt.title('The elbow method')
            plt.xlabel('Number of clusters')
            plt.ylabel('WCSS')  # within cluster sum of squares
            plt.savefig(r"SKlearn/clustring/images/elbow.png")
            plt2.clf()
            return kn.elbow

    def saveModel(self,kmeansModel,filename):
        filename = filename
        joblib.dump(kmeansModel, filename)

    def predict(self, modelname,predictList):
        model_loaded = joblib.load(modelname)
        l = predictList
        #print(np.array(l).reshape(-1, len(l)))
        belongCluster = model_loaded.predict(np.array(l).reshape(-1, len(l)))
        return belongCluster

    def kmeansEvaluation(self,kmeans):
        # Calculating Details
        print('KMeansModel centers are : ', kmeans.cluster_centers_)
        print('KMeansModel labels are : ', kmeans.labels_)
        print('KMeansModel intertia is : ', kmeans.inertia_)
        print('KMeansModel No. of iteration is : ', kmeans.n_iter_)


    def plotKMeans(self,kmeans,y_kmeans,clustringImageName):
        colorList= ["red", "blue", "green", "pink", "black", "orange", "purple", "beige", "brown", "gray", "cyan", "magenta"]
        #colorList = ['r','b','g','c']
        labels = np.unique(kmeans.labels_)
        for i in labels:
            plt2.scatter(self.data[y_kmeans == i, 0], self.data[y_kmeans == i, 1], s=10, c=colorList[i])
            # print("value of i:",i)
        plt2.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s = 300, c = 'y')
        plt2.title('Clusters of customers')
        plt2.xlabel('Annual Income (k$)')
        plt2.ylabel('Spending Score (1-100)')
        print(str('km'+clustringImageName))
        plt2.savefig(r"SKlearn/clustring/images/"+str(clustringImageName))
        plt2.clf()

