import pandas as pd
import numpy as np

class DataFrameInfo:

    def get_stats(self, dataframe):
        #stats = dataframe.describe(include='all')
        stats = dataframe.describe()
        return stats

    def check_data_type(self, dataframe):
        data_type = dataframe.dtypes
        return data_type  
    
    def get_mean(self, dataframe, column):
        mean = dataframe[column].mean(numeric_only = True)
        return mean

    def get_median(self, dataframe, column):
        median = dataframe[column].median(numeric_only = True)
        return median

    def get_mode(self, dataframe, column):
        mode = dataframe[column].mode()
        return mode
 
    def get_std_dev(self, dataframe, column):
        stdev = dataframe[column].std(numeric_only = True)
        return stdev
    

    def get_distinct_count(self, dataframe, column):
        count = dataframe[column].nunique()
        return count
    
    def get_unique_values(self, dataframe, column):
        '''This method returns the unique values of the give dataframe columns'''

        return dataframe[column].unique()
    
    def print_shape(self, dataframe):
        shape = dataframe.shape
        print(f'The shape of the dataframe is {shape}.')
    

    def null_count(self, dataframe, info=True):
        number_of_records = len(dataframe)
        if info:
            print(f'There are {number_of_records} records in the database. The number of nulls in each column are: ')

        number_missing = dataframe.isna().sum()
        return number_missing

    def null_count_percentage(self, dataframe):

        print('Percentage of values which are null in each column: ')

        percentage_missing = round((dataframe.isna().sum() / len(dataframe) * 100), 2)
        return percentage_missing
    
    def null_counts(self, dataframe):
        ''' This method returns a dataframe containing null counts and percentage of nulls of columns. 
        Columns that have no nulls are filterd out'''

        number_of_records = len(dataframe) 
        print(f'There are {number_of_records} records in the database.\nThe columns that contain nulls are listed below along with their null counts/percentages.')

        missing_values = pd.DataFrame(dataframe.isna().sum(), columns=['Null_Count'])
        missing_values['Percentage_of_Nulls'] = round((dataframe.isna().sum() / number_of_records * 100), 2)

        return missing_values[missing_values['Null_Count']>0]
    
    def get_numeric_columns(self, dataframe, exclude=None):
        '''This method returns a list of columns in a dataframe that are numeric, excluding
         any columns given in the exclude argument '''

        numeric_columns = dataframe.select_dtypes(include=np.number).columns.tolist()

        if exclude:
            for name in exclude:
                if name in numeric_columns:
                    numeric_columns.remove(name)
                    
        return numeric_columns
