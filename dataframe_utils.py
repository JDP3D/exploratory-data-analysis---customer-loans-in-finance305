from scipy import stats
import numpy as np
import pandas as pd

class DataFrameTransform:
    
    def drop_columns(self, dataframe, column):    
        '''
        This method drops the specified columns from a dataframe

        Parameters:
            dataframe: The dataframe to which this method will be applied.
            column: The name(s) of columns that will be dropped from the dataframe

        Returns:
            dataFrame: The updated dataframe.
        '''
        return dataframe.drop(axis=1, columns=column)
    
    def drop_nulls(self, dataframe, how='any',columns=None): 
        ''' This method drops rows with nulls depending on the given criteria

        Parameters:
            dataframe: The dataframe to which this method will be applied.
            column: The name(s) of columns that nulls will be dropped from

        Returns:
            dataFrame: The updated dataframe.
        
        '''
        df_shape = dataframe.shape
        new_df = dataframe.dropna(how=how, subset=columns)
        no_rows_removed = df_shape[0] - new_df.shape[0]
        print(f'{no_rows_removed} rows have been removed from the dataframe.')
        return new_df
    
    def drop_nulls_threshold(self, dataframe, thresh):
        ''' This method drops columns with nulls depending on the threshold 
        given as a percentage of nulls

        Parameters:
            dataframe: The dataframe to which this method will be applied.
            threshold: The percentage of nulls over (inclusive) which the columns will be dropped.

        Returns:
            dataFrame: The updated dataframe.  

        '''
        threshold = int((1-thresh)*len(dataframe)) + 1
        df_shape = dataframe.shape
        new_df = dataframe.dropna(axis=1, thresh=threshold)
        no_columns_removed = df_shape[1] - new_df.shape[1]
        print(f'{no_columns_removed} columns have been removed from the dataframe.')
        return new_df
    
    def fill_nulls(self, dataframe, columns, value):
        '''This method fills the nulls of  specied columns with the given value.

        Parameters:
            dataframe: The dataframe to which this method will be applied.
            column: The name(s) of columns that will be dropped from the dataframe.
            value: The value that the null will be replaced with

        Returns:
            dataFrame: The updated dataframe.
        
        '''

        return dataframe[columns].fillna(value)

    def impute_mean(self, dataframe, columns):
        '''This method fills null values with the mean value of a column
        
        Parameters:
            dataframe: The dataframe to which this method will be applied.
            column: The name(s) of columns that will be imputed

        Returns:
            dataFrame: The updated dataframe.
        
        '''
        return dataframe[columns].fillna(dataframe[columns].mean(numeric_only = True))

    def impute_median(self, dataframe, columns):
        '''This method fills null values with the mean value of a column'
        
         Parameters:
            dataframe: The dataframe to which this method will be applied.
            column: The name(s) of columns that will be imputed

        Returns:
            dataFrame: The updated dataframe.
        
        '''
        return dataframe[columns].fillna(dataframe[columns].median(numeric_only = True))
    
    def impute_mode(self, dataframe, columns):
        '''This method fills null values with the mode value of a column'''

        return dataframe[columns].fillna(dataframe[columns].mode()[0])
    
    
    def log_transform(self, dataframe, column):
        '''This method tranforms data using a log transformation.
        
        Parameters:
            dataframe: The dataframe to which this method will be applied.
            column: The name of the column that will be transformed

        Returns:
            dataFrame: The updated dataframe.
        
        '''
        return dataframe[column].map(lambda i: np.log(i) if i > 0 else 0)
    

    def box_cox_transform(self, dataframe, column):

        '''
        This method tranforms data using a Box-Cox transformation.

        Parameters:
            dataframe: The dataframe to which this method will be applied.
            column: The name of the column that will be transformed

        Returns:
            boxcox: The transformed column.
        '''
        boxcox = stats.boxcox(dataframe[column])
        boxcox = pd.Series(boxcox[0])
        return boxcox
    
    def yeo_johnson_transform(self, dataframe, column):

        '''
        This method tranforms data using a Yeo-Johnson transformation.

        Parameters:
            dataframe: The dataframe to which this method will be applied.
            column: The name of the column that will be transformed

        Returns:
            yeojohnson: The transformed column.
        '''
        yeojohnson = stats.yeojohnson(dataframe[column])
        yeojohnson = pd.Series(yeojohnson[0])
        return yeojohnson
    
    def transform_compare(self, dataframe, column):
        '''This method is used to test the effects of log, Box-Cox and Yeo-Johnson transformations.

        Parameters:
            dataframe: The dataframe to which this method will be applied.
            column: The name of the column that will be transformed.
        
        Returns: Prints out the results.

        '''
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
        a given column
        
        Parameters:
            dataframe: The dataframe to which this method will be applied.
            column: The name of the column that will be tested.
            threshold: the z-score threshold.

        Returns: The updated dataframe 
        '''
        zscores = stats.zscore(dataframe[column])
        return dataframe[abs(zscores) <= threshold]
    
    def zscore_test(self, dataframe, column, threshold):
        '''this method tests for zscores within a given threshold and
          returns them as a pandas series 
          
          Parameters:
            dataframe: The dataframe to which this method will be applied.
            column: The name of the column that will be tested.
            threshold: the z-score threshold.

          Returns: A series containg the z-scores     
          '''
        zscores = stats.zscore(dataframe[column])
        return zscores[abs(zscores)>threshold]
    
    def iqr_outlier_test(self, dataframe, column):
        '''This method returns the outliers of a column using the standard IQR test (1.5 times).
        
        Parameters:
            dataframe: The dataframe to which this method will be applied.
            column: The name of the column that will be tested.

          Returns: prints out the values of the outliers in a column 
        
        '''
        values = dataframe[column]
        Q1 = values.quantile(0.25)
        Q3 = values.quantile(0.75)

        # Calculate IQR
        IQR = Q3 - Q1
        outliers = values[(values < (Q1 - 1.5 * IQR)) | (values > (Q3 + 1.5 * IQR))]
        print(f'There are {len(outliers)} outliers in {column}.')
        
        return outliers
    
    ## Only relevent to loans database used in this project
    # def get_expected_revenue(self, dataframe):
    #     '''This method calculates the expected revenue for each customer in the dataframe.
        
    #     Parameters:
    #         dataframe: The dataframe to which the method will be applied to

    #     Returns:
    #         series containing the expected values
        
    #     '''
    #     return dataframe['term'] * dataframe['instalment']