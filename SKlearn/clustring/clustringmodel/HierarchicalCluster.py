import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import pandas as pd
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import joblib

class HierarchicalCluster():

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
            #print(self.data )
            print(self.data.shape)

    def createmodel(self,k=2,method="elbow" ,affinity = 'euclidean',linkage = 'ward', OutputFileName=""):

        hierarchicalcluster = AgglomerativeClustering(n_clusters=k,  affinity = affinity,linkage = linkage )
        y_HCModel = hierarchicalcluster.fit_predict(self.data)
        locValue : int = len(self.dataset.columns)
        self.dataset.insert(loc=locValue ,column='cluster output',value=y_HCModel)
        OutputFile =f"SKlearn/clustring/outputFiels/{OutputFileName}output.csv"
        self.dataset.to_csv(OutputFile, index=False)
        numberOfK = k
        return hierarchicalcluster,y_HCModel , numberOfK

    def drawDendoGram(self):
        dendrogram = sch.dendrogram(sch.linkage(self.data , method='ward'))
        plt.title('Dendrogram')
        plt.xlabel('Customers')
        plt.ylabel('Euclidean distances')
        plt.savefig(r"SKlearn/clustring/images/Dendrogram.png")
        plt2.clf()
        plt.show()


    def saveModel(self,kmeansModel,filename):
        filename = filename
        joblib.dump(kmeansModel, filename)

    def predictmodel(self, modelname,predictList):
        model_loaded = joblib.load(modelname)
        l = predictList
        #print(np.array(l).reshape(-1, len(l)))
        belongCluster = model_loaded.predict(np.array(l).reshape(-1, len(l)))
        return belongCluster

    def hierarchicalclusterEvaluation(self,hierarchicalclusterModel):
        # Calculating Details
        print('hierarchicalclusterModel centers are : ', hierarchicalclusterModel.n_clusters)
        print('hierarchicalclusterModel labels are : ', hierarchicalclusterModel.labels_)

    def plotKMeans(self,HCModel,y_HCModel,clustringImageName):
        colorList= ["red", "blue", "green", "pink", "black", "orange", "purple", "beige", "brown", "gray", "cyan", "magenta"]
        #colorList = ['r','b','g','c']
        labels = np.unique(HCModel.labels_)
        for i in labels:
            plt2.scatter(self.data[y_HCModel == i, 0], self.data[y_HCModel == i, 1], s=10, c=colorList[i],label = 'Cluster '+str(i))
            # print("value of i:",i)
        # plt2.scatter(kmeans.cluster_centers_[:, 0], HCModel.cluster_centers_[:, 1], s = 300, c = 'y')
        plt2.title('Clusters of customers')
        plt2.xlabel('Annual Income (k$)')
        plt2.ylabel('Spending Score (1-100)')
        plt2.legend()
        print(str('km'+clustringImageName))
        plt2.savefig(r"SKlearn/clustring/images/"+str(clustringImageName))
        plt2.clf()