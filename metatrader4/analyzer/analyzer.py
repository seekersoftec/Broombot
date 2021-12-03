#
import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import (AdaBoostRegressor,  # Adaboost regressor
                              RandomForestRegressor,  # Random forest regressor
                              GradientBoostingRegressor,  # Gradient boosting
                              BaggingRegressor,  # Bagging regressor
                              StackingRegressor,  # Stacking regressor
                              ExtraTreesRegressor)  # Extratrees regressor
#
# Data from investing.com
#


class Twenty_Pips:
    """
        20 pips Challenge
    """

    def __init__(self, filepath) -> None:
        self.pips_sheet = pd.read_excel(filepath)
        print(self.pips_sheet)
        pass
    pass
#
#
#
# Feature scaling


class PreprocessDataFrame():
    def __init__(self, dataframe, test_size=0.25, features_size=1, target_size=1):
        """
          Preprocess the dataset. 
        """
        # self.dataframe = self.cleanNullValues(dataframe)
        self.dataframe = dataframe
        self.test_size = test_size
        self.feature_vector = self.dataframe.iloc[:, :features_size].values
        self.target_vector = self.dataframe.iloc[:, target_size:].values
        # self.target_vector = self.dataframe.iloc[:, :target_size].values

    # clean null values
    def cleanNullValues(self, dataframe):
        # determining the null values in each column
        dataframe = dataframe.replace("?", np.nan)
        for column in dataframe.columns:
            dataframe[column] = dataframe[column].fillna(
                dataframe[column].median())

        return dataframe

    #
    def standardScaler(self):
        # Get the feature vector
        X = self.feature_vector

        # Get the target vector
        y = self.target_vector

        # Encoding categorical data values
        # labelencoder_Y = LabelEncoder()
        # y = labelencoder_Y.fit_transform(y)

        #
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size)

        # Declare the standard scaler
        std_scaler = StandardScaler()

        std_scaler.fit(X_train)

        # Standardize the training set
        # X_train = std_scaler.fit_transform(X_train)
        X_train = std_scaler.transform(X_train)

        # Standardize the testing set
        # X_train = std_scaler.fit_transform(X_train)
        X_test = std_scaler.transform(X_test)

        #
        return X_train, X_test, y_train, y_test

    #
    def minMaxScaler(self):
        # Get the feature vector
        X = self.feature_vector

        # Get the target vector
        y = self.target_vector

        # splitting the dataset into  training and test set
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size)

        # MinMaxScaling
        mm = MinMaxScaler(feature_range=(0, 1))

        # feeding the independent data into the scaler

        # Standardize the training set
        X_train = mm.fit_transform(X_train)
        # X_train = mm.transform(X_train)

        # Standardize the testing set
        X_test = mm.fit_transform(X_test)
        # X_test = mm.transform(X_test)

        #
        return X_train, X_test, y_train, y_test


class Analyzer:
    """
        Analyze data
    """

    def __init__(self, _currency) -> None:
        self.historical_data = _currency.retrieve_historical_data(
            from_date='01/01/2016', to_date='01/01/2020')
        # print(historical_data)
        #
        self.technical_indicators = _currency.retrieve_technical_indicators(
            interval='1hour')
        # print(technical_indicators)
    pass

    def _historical_analysis(self):

        pass


#
#
#
#
# Twenty_Pips('../data/20_pips_challenge.xlsx')
#
# df.iloc[:, df.columns.size-4:]
# target = ['Hinselmann', 'Citology','Schiller','Biopsy']
#
# X_train, X_test, y_train, y_test = PreprocessDataFrame(dataframe=df, test_size=0.10, target_size=df.columns.size-1, features_size=df.columns.size-1).standardScaler()
# X_train, X_test, y_train, y_test = PreprocessDataFrame(dataframe=df, test_size=0.40, target_size=df.columns.size-1, features_size=df.columns.size-1).minMaxScaler()
#
# print(X_train.shape)
# print(X_test.shape)
# print(y_train.shape)
# print(y_test.shape)
