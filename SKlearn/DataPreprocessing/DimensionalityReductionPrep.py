from sklearn.decomposition import FactorAnalysis
from sklearn.decomposition import FastICA
from sklearn.manifold import TSNE
from sklearn import decomposition
from sklearn import manifold
from sklearn import datasets
import pandas as pd
import numpy as np


class DimensionalityReductionPrep():
    def __init__(self, df, n_components, dimRedHandelingMethod):
        self.df = df.values
        self.n_components = n_components
        self.handelingMethod = dimRedHandelingMethod

    def FactorAnalysis(self):
        FA = FactorAnalysis(n_components=self.n_components).fit_transform(self.df)
        newDF = pd.DataFrame(FA)
        return newDF

    def Pca(self):
        pca = decomposition.PCA(n_components=self.n_components).fit_transform(self.df)
        newDF = pd.DataFrame(pca)
        return newDF

    def Ica(self):
        ica = FastICA(n_components=self.n_components, random_state=12).fit_transform(self.df)
        newDF = pd.DataFrame(ica)
        return newDF

    def Isomap(self):
        ica = manifold.Isomap(n_neighbors=5, n_components=self.n_components).fit_transform(self.df)
        newDF = pd.DataFrame(ica)
        return newDF

    def Tsne(self):
        tsne = TSNE(n_components=self.n_components, n_iter=300).fit_transform(self.df)
        newDF = pd.DataFrame(tsne)
        return newDF

    def handelingDimRed(self):
        if self.handelingMethod == 'FA':
            print("FA")
            return self.FactorAnalysis()
        elif self.handelingMethod == 'PCA':
            print("PCA")
            return self.Pca()
        elif self.handelingMethod == 'ICA':
            print("ICA")
            return self.Ica()
        elif self.handelingMethod == 'ISOMAP':
            print("ISOMAP")
            return self.Isomap()
        elif self.handelingMethod == 'TSNE':
            print("TSNE")
            return self.Tsne()