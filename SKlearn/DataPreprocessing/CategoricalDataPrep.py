import category_encoders as ce
import pandas as pd


class CategoricalData:

    def OneHotEncoding(self, df, columnList=[]):
        encoder = ce.OneHotEncoder(cols=columnList, handle_unknown='return_nan', return_df=True, use_cat_names=True)
        df_encoded = encoder.fit_transform(df)
        return df_encoded

    def EffectEncoding(self, df, columnList=[]):
        encoder = ce.sum_coding.SumEncoder(cols=columnList, verbose=False)
        df_encoded = encoder.fit_transform(df)
        return df_encoded

    def BinaryEncoder(self, df, columnList=[]):
        encoder = ce.BinaryEncoder(cols=columnList, return_df=True)
        df_encoded = encoder.fit_transform(df)
        return df_encoded

    def HandelCategoricalData(self, df, category_encoder_method):
        columnList = df.select_dtypes(include=['object']).columns.tolist()
        print(columnList)
        if (category_encoder_method == "OneHotEncoding"):
            print("OneHotEncoding")
            newdf = self.OneHotEncoding(df, columnList=columnList)
            return newdf
        elif (category_encoder_method == "EffectEncoding"):
            newdf = self.EffectEncoding(df, columnList=columnList)
            return newdf
        elif (category_encoder_method == "BinaryEncoder"):
            newdf = self.BinaryEncoder(df, columnList=columnList)
            return newdf