import pandas as pd
from scipy import stats
import numpy as np

class DataFrameTransform:
    
    def drop_columns(self, dataframe, column):
        '''This method drops the specified columns from a dataframe'''

        return dataframe.drop(axis=1, columns=column)
    
    def drop_nulls(self, dataframe, how='any',columns=None):
        ''' This method drops rows with nulls depending on the given criteria'''

        df_shape = dataframe.shape
        new_df = dataframe.dropna(how=how, subset=columns)
        no_rows_removed = df_shape[0] - new_df.shape[0]
        print(f'{no_rows_removed} rows have been removed from the dataframe.')
        return new_df
    
    def drop_nulls_threshold(self, dataframe, thresh):
        ''' This method drops columns with nulls depending on the threshold given as a percentage of nulls'''

        threshold = int((1-thresh)*len(dataframe)) + 1
        df_shape = dataframe.shape
        new_df = dataframe.dropna(axis=1, thresh=threshold)
        no_columns_removed = df_shape[1] - new_df.shape[1]
        print(f'{no_columns_removed} columns have been removed from the dataframe.')
        return new_df
    
    def fill_nulls(self, dataframe, columns, value):
        '''This method fills the nulls of  specied columns with the given value'''

        return dataframe[columns].fillna(value)

    def impute_mean(self, dataframe, columns):
        '''This method fills null values with the mean value of a column'''

        return dataframe[columns].fillna(dataframe[columns].mean(numeric_only = True))

    def impute_median(self, dataframe, columns):
        '''This method fills null values with the mean value of a column'''

        return dataframe[columns].fillna(dataframe[columns].median(numeric_only = True))
    
    def impute_mode(self, dataframe, columns):
        '''This method fills null values with the mode value of a column'''

        return dataframe[columns].fillna(dataframe[columns].mode()[0])
    
    
    def log_transform(self, dataframe, column):
        '''This method tranforms data using a log transform'''

        return dataframe[column].map(lambda i: np.log(i) if i > 0 else 0)
    

    def box_cox_transform(self, dataframe, column):

        '''
        This method is used to apply Box-Cox transformation to normalise a column.

        Parameters:
            dataFrame (pd.DataFrame): The dataframe to which this method will be applied.
            column(str): The name of the column which will be transformed.

        Returns:
            boxcox (pd.Series): The transformed column.
        '''

        boxcox = stats.boxcox(dataframe[column])
        boxcox = pd.Series(boxcox[0])
        return boxcox
    
    def yeo_johnson_transform(self, dataframe, column):

        '''
        This method is used to apply Yeo-Johnson transformation to normalise a column.

        Parameters:
            DataFrame (pd.DataFrame): The dataframe to which this method will be applied.
            column_name (str): The name of the column which will be transformed.

        Returns:
            yeojohnson_column (pd.Series): The transformed column.
        '''

        yeojohnson = stats.yeojohnson(dataframe[column])
        yeojohnson = pd.Series(yeojohnson[0])
        return yeojohnson
    
    def transform_compare(self, dataframe, column):
        '''This method prints out the skew after applying transforms '''

        original_skew = dataframe[column].skew()
        print(f'Original skew: {round(original_skew, 2)}')

        log = self.log_transform(dataframe, column)
        log_skew = round(log.skew(), 2)
        print(f'Skew after log transform: {log_skew}')

        if dataframe[column].min() <= 0:
            print("Cannot perform Box-Cox transform as data isn't strictly positive")
        else:
            box = self.box_cox_transform(dataframe, column)
            box_skew = round(box.skew(), 2) #type: ignore
            print(f'Skew after Box-Cox transform: {box_skew}')

        yeo = self.yeo_johnson_transform(dataframe, column)
        yeo_skew = round(yeo.skew(), 2) #type: ignore
        print(f'Skew after Yeo-Johnson transform: {yeo_skew}')

    def drop_outliers_zscore(self, dataframe, column, threshold):
        '''This method drops rows from a dataframe depending on the z-score of
        a given column'''
        zscores = stats.zscore(dataframe[column])
        return dataframe[abs(zscores) <= threshold]
    
    def zscore_test(self, dataframe, column, threshold):
        '''this method tests for zscores within a given threshold and
          returns them as a pandas series '''

        zscores = stats.zscore(dataframe[column])
        return zscores[abs(zscores)>threshold]
    
    def iqr_outlier_test(self, dataframe, column):
        '''This method returns the outliers of a column using the standard IQR test (1.5 times)'''
    
        values = dataframe[column]
        Q1 = values.quantile(0.25)
        Q3 = values.quantile(0.75)

        # Calculate IQR
        IQR = Q3 - Q1
        outliers = values[(values < (Q1 - 1.5 * IQR)) | (values > (Q3 + 1.5 * IQR))]
        print(f'There are {len(outliers)} outliers in {column}.')
        
        return outliers