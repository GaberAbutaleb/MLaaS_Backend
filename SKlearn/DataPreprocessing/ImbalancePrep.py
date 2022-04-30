from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import EditedNearestNeighbours
from imblearn.under_sampling import TomekLinks
from imblearn.under_sampling import NearMiss
from sklearn.metrics import brier_score_loss
from collections import Counter
import pandas as pd
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class DataBalance:
    def __init__(self, dataFrame=None, target=None):
        if dataFrame is not None and target is not None:
            if not (type(dataFrame) == pd.DataFrame):
                self.dataFrame = pd.DataFrame(dataFrame)
            else:
                self.dataFrame = dataFrame

            self.target = target
            self.X = dataFrame.drop(target, axis=1)
            self.y = dataFrame[target]
            self.originalY = self.y

    def describe(self):
        print('Class Distribution: \n', self.y.value_counts())
        # visualize the target variable
        g = sns.countplot(self.y)
        g.set_xticklabels(['Good','Bad'])
        plt.show()

    def recommend_technique(self):
        val_conts = self.y.value_counts()
        if (val_conts.values.max() - val_conts.values.min()) < (0.1 * len(self.y)):
            print("under")
            return 'TomLinks'
        else:
            print("over")
            return 'SMOTE'
        return

    def balance(self, technique='RCMND'):
        if technique == 'RCMND':
            technique = self.recommend_technique()
        if technique == 'OVER':
            sample = RandomOverSampler(sampling_strategy='minority')
        elif technique == 'UNDER':
            sample = RandomUnderSampler(sampling_strategy='majority')
        elif technique == 'SMOTE':
            sample = SMOTE(sampling_strategy='auto',k_neighbors=5)
        elif technique == 'ENN':
            sample = EditedNearestNeighbours(sampling_strategy='auto', n_neighbors=3, kind_sel='all')
        elif technique =="TomLinks":
            sample = TomekLinks(sampling_strategy='majority')
        elif technique == "NearMiss" :
            sample = NearMiss()
        self.X, self.y= sample.fit_resample(self.X, self.y)
        print('Data Resampled Successfuly Using ', technique)
        print('original dataset shape:', Counter(self.originalY))
        print('Resample dataset shape', Counter( self.y))
        if self.dataFrame is not None and self.target is not None:
            return pd.concat([ self.X, self.y], axis=1)