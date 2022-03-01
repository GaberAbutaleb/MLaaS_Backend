import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator
import joblib



class DBScan():

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

    def createmodel(self, k=0,minSamples = 10, OutputFileName=""):

        if k== 0:
            eps = self.bestK()
        else:
            eps = k
        dbscan_cluster = DBSCAN(eps=eps, min_samples=minSamples)
        dbscan_cluster.fit(self.data)
        # Number of Clusters
        labels = dbscan_cluster.labels_
        N_clus = len(set(labels)) - (1 if -1 in labels else 0)
        print('Estimated no. of clusters: %d' % N_clus)
        # Identify Noise
        n_noise = list(dbscan_cluster.labels_).count(-1)
        print('Estimated no. of noise points: %d' % n_noise)
        locValue: int = len(self.dataset.columns)
        self.dataset.insert(loc=locValue, column='cluster output', value=labels)
        OutputFile = f"SKlearn/clustring/outputFiels/{OutputFileName}output.csv"
        self.dataset.to_csv(OutputFile, index=False)
        epsvalue = eps
        return dbscan_cluster, labels, N_clus, epsvalue

    def bestK(self):
        data_frame = self.data

        nearest_neighbors = NearestNeighbors(n_neighbors=11)
        neighbors = nearest_neighbors.fit(data_frame)
        distances, indices = neighbors.kneighbors(data_frame)
        distances = np.sort(distances[:, 10], axis=0)
        i = np.arange(len(distances))
        knee = KneeLocator(i, distances, S=1, curve='convex', direction='increasing', interp_method='polynomial')
        print("The best k from elbow",distances[knee.knee])
        # fig = plt.figure(figsize=(5, 5))
        # knee.plot_knee()
        # plt.xlabel("Points")
        # plt.ylabel("Distance")
        # # plt.show()
        # plt.savefig(r"SKlearn/clustring/images/elbow.png")
        # plt2.clf()
        return distances[knee.knee]

    def saveModel(self,DBScanModel,filename):
        filename = filename
        joblib.dump(DBScanModel, filename)


    def plotDBScan(self, dbscan_cluster, y_kmeans, clustringImageName):
        colorList = ["blue", "black", "yellow", "green", "pink", "orange", "purple", "beige", "brown", "gray",
                         "cyan", "magenta", "salmon", "silver", "yellowgreen", "navy", "orchid", "maroon", "darkblue",
                         "coral", "gold", "lime", "tan", "teal"]
        y_kmeans = dbscan_cluster.labels_
        labels = np.unique(dbscan_cluster.labels_)
        for i in labels:
            if i != -1:
                plt.scatter(self.data[y_kmeans == i, 0], self.data[y_kmeans == i, 1], s=10, c=colorList[i])
            elif i == -1:
                plt.scatter(self.data[y_kmeans == i, 0], self.data[y_kmeans == i, 1], s=10, c="red")
        plt2.title('DBScan Cluster output')
        plt2.xlabel('X')
        plt2.ylabel('y')
        print(str('dbsc' + clustringImageName))
        plt2.savefig(r"SKlearn/clustring/images/" + str(clustringImageName))
        plt2.clf()