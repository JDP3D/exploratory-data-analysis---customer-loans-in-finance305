import pandas as pd
import numpy as np

class DataFrameInfo:

    def get_stats(self, dataframe):
        '''
        This method prints out the statistics of the dataframe
        
        Parameters:
            dataframe: The dataframe from which to get the statistics from.
        
        Returns:
            Prints out the statistics of the dataframe.
        
        '''
        stats = dataframe.describe()
        return stats

    def check_data_type(self, dataframe):
        '''
        This method prints out the data types of the dataframe
        
        Parameters:
            dataframe: The dataframe from which to get the statistics from.
        
        Returns:
            Prints out the data types of the dataframe.
        
        '''
        data_type = dataframe.dtypes
        return data_type  
    
    def get_mean(self, dataframe, column):
        '''
        This method retrieves the mean of the dataframe column
        
        Parameters:
            dataframe: The dataframe from which to get the statistics from.
            column: The required column of the dataframe
        
        Returns:
            The mean of the dataframe column.
        
        '''
        
        mean = dataframe[column].mean(numeric_only = True)
        return mean

    def get_median(self, dataframe, column):
        '''
        This method retrieves the median of the dataframe column
        
        Parameters:
            dataframe: The dataframe from which to get the statistics from.
            column: The required column of the dataframe
        
        Returns:
            The median of the dataframe column.
        
        '''
        median = dataframe[column].median(numeric_only = True)
        return median

    def get_mode(self, dataframe, column):
        '''
        This method retrieves the mode of the dataframe column
        
        Parameters:
            dataframe: The dataframe from which to get the statistics from.
            column: The required column of the dataframe
        
        Returns:
            The mode of the dataframe column.
        
        '''
        mode = dataframe[column].mode()
        return mode
 
    def get_std_dev(self, dataframe, column):
        '''
        This method retrieves the standard deviation of the dataframe column
        
        Parameters:
            dataframe: The dataframe from which to get the statistics from.
            column: The required column of the dataframe
        
        Returns:
            The median of the dataframe column.
        
        '''
        stdev = dataframe[column].std(numeric_only = True)
        return stdev
    

    def get_distinct_count(self, dataframe, column):
        '''
        This method comutes the count of distinct values of a dataframe column.
        
        Parameters:
            dataframe: The dataframe from which to get the statistics from.
            column: The required column of the dataframe
        
        Returns:
            The count of distinct values in the column.
        
        '''
        count = dataframe[column].nunique()
        return count
    
    def get_unique_values(self, dataframe, column):
        '''This method returns the unique values of the give dataframe columns
        
         Parameters:
            dataframe: The dataframe from which to get the statistics from.
            column: The required column of the dataframe
        
        Returns:
            The unique values in the column.
        
        '''
        return dataframe[column].unique()
    
    def print_shape(self, dataframe):
        '''This method prints the shape of a dataframe.
        
         Parameters:
            dataframe: The dataframe from which to get the statistics from.
    
        Returns:
            The shape of the dataframe.
        
        '''
        shape = dataframe.shape
        print(f'The shape of the dataframe is {shape}.')
    

    def null_count(self, dataframe, info=True):
        '''This method computes the null counts in a dataframe
        
        Parameters:
            dataframe: The required dataframe.
        
        Returns:
            The null count

        '''
        number_of_records = len(dataframe)
        if info:
            print(f'There are {number_of_records} records in the database. The number of nulls in each column are: ')

        number_missing = dataframe.isna().sum()
        return number_missing

    def null_count_percentage(self, dataframe):
        '''This method computes the percentage of nulls in a dataframe
        
        Parameters:
            dataframe: The required dataframe.
        
        Returns:
            The null percentage.

        '''

        print('Percentage of values which are null in each column: ')

        percentage_missing = round((dataframe.isna().sum() / len(dataframe) * 100), 2)
        return percentage_missing
    
    def null_counts(self, dataframe):
        ''' This method returns a dataframe containing null counts and percentage of
        nulls of columns. Columns that have no nulls are filterd out
        
        Parameters:
            dataframe: The required dataframe.
        
        Returns:
            A dataframe of the null precentage/counts.
        '''
        number_of_records = len(dataframe) 
        print(f'There are {number_of_records} records in the database.\nThe columns that contain nulls are listed below along with their null counts/percentages.')

        missing_values = pd.DataFrame(dataframe.isna().sum(), columns=['Null_Count'])
        missing_values['Percentage_of_Nulls'] = round((dataframe.isna().sum() / number_of_records * 100), 2)

        return missing_values[missing_values['Null_Count']>0]
    
    def get_numeric_columns(self, dataframe, exclude=None):
        '''This method returns a list of columns in a dataframe that are numeric, excluding
         any columns given in the exclude argument 
         
         Parameters:
            dataframe: The required dataframe.
            exclude: columns to remove from the list
        
        Returns:
            A list of numeric columns.
         
         '''
        numeric_columns = dataframe.select_dtypes(include=np.number).columns.tolist()

        if exclude:
            for name in exclude:
                if name in numeric_columns:
                    numeric_columns.remove(name)
                    
        return numeric_columns
