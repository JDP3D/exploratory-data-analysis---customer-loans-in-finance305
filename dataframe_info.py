import pandas as pd
import numpy as np

class DataFrameInfo:

    def get_stats(self, dataframe: pd.Series | pd.DataFrame) -> pd.Series | pd.DataFrame:
        '''
        This method prints out the statistics of the dataframe
        
        Parameters:
            dataframe: The required dataframe.
        
        Returns:
            Returns the statistics of the dataframe.
        
        '''
        stats = dataframe.describe()
        return stats

    def check_data_type(self, dataframe: pd.DataFrame) -> pd.Series:
        '''
        This method prints out the data types of the dataframe
        
        Parameters:
            dataframe: The required dataframe.
        
        Returns:
            returns a pandas series of the data types in the dataframe.
        
        '''
        data_type = dataframe.dtypes
        return data_type  
    
    def get_mean(self, dataframe: pd.DataFrame, column: str | list[str]) -> float | pd.Series:
        '''
        This method retrieves the mean of the dataframe column/s
        
        Parameters:
            dataframe: The required dataframe.
            column: The required column of the dataframe. Can be just one column 
            given as a string or a list of columns.
        
        Returns:
            A float or pandas series containing the mean/s of the given dataframe column/s.
        
        '''
        
        mean = dataframe[column].mean(numeric_only = True)
        return mean

    def get_median(self, dataframe: pd.DataFrame, column: str | list[str]) -> float | pd.Series:
        '''
        This method retrieves the median of the dataframe column/s
        
        Parameters:
            dataframe: The required dataframe.
            column: The required column of the dataframe. Can be just one column 
            given as a string or a list of columns.
        
        Returns:
            A float or pandas series containing the median/s of the given column/s.
        
        '''
        median = dataframe[column].median(numeric_only = True)
        return median

    def get_mode(self, dataframe: pd.DataFrame, column: str | list[str]) -> pd.Series | pd.DataFrame:
        '''
        This method retrieves the mode of the dataframe column
        
        Parameters:
            dataframe: The required dataframe.
            column: The required column of the dataframe. Can be just one column 
            given as a string or a list of columns.

        Returns:
            A pandas dataframe containing the mode/s of the given column/s.
        
        '''
        mode = dataframe[column].mode()
        return mode 
 
    def get_std_dev(self, dataframe: pd.DataFrame, column: str | list[str]) -> float | pd.Series:
        '''
        This method retrieves the standard deviation of the dataframe column/s.
        
        Parameters:
            dataframe: The required dataframe.
            column: The required column of the dataframe. Can be just one column 
            given as a string or a list of columns.
        
        Returns:
            A  float or pandas series containing the standard deviation/s of the given column/s.
        
        '''
        stdev = dataframe[column].std(numeric_only = True)
        return stdev
    

    def get_distinct_count(self, dataframe: pd.DataFrame, column: str | list[str]) -> int | pd.Series:
        '''
        This method retrieves the count/s of distinct values of a dataframe column/s.
        
        Parameters:
            The required dataframe.
            column: The required column of the dataframe. Can be just one column 
            given as a string or a list of columns.
        
        Returns:
            An int or pandas series containg the count of distinct values in the column/s.
        
        '''
        count = dataframe[column].nunique()
        return count
    
    def get_unique_values(self, dataframe: pd.DataFrame, column: str) -> np.ndarray:
        '''
        This method returns the unique values of the give dataframe columns
        
         Parameters:
            dataframe: The required dataframe.
            column: The required column of the dataframe.
        
        Returns:
            An array of the unique values in the column.
        
        '''
    
        unique = dataframe[column].unique()
        return unique
    
    def print_shape(self, dataframe: pd.DataFrame) -> None:
        '''
        This method prints the shape of a dataframe.
        
         Parameters:
            dataframe: The required dataframe.
    
        Returns:
            Prints the shape of the dataframe.
        
        '''
        shape = dataframe.shape
        print(f'The shape of the dataframe is {shape}.')
    

    def null_count(self, dataframe: pd.Series | pd.DataFrame, info: bool=True) -> int | pd.Series:
        '''
        This method computes the null counts in a dataframe.
        
        Parameters:
            dataframe: The required dataframe.
            info: If info is true the method will print out the number of
            rows in the database. Default = True.
        
        Returns:
            A pandas series of the null counts.

        '''
        number_of_records = len(dataframe)
        if info:
            print(f'There are {number_of_records} records in the database. The number of nulls in each column are: ')

        number_missing = dataframe.isna().sum()
        return number_missing

    def null_count_percentage(self, dataframe: pd.DataFrame) -> pd.Series:
        '''
        This method computes the percentage of nulls in a dataframe
        
        Parameters:
            dataframe: The required dataframe.
        
        Returns:
            A series containing the percentage of nulls in each column.

        '''

        print('Percentage of values which are null in each column: ')

        percentage_missing = round((dataframe.isna().sum() / len(dataframe) * 100), 2)
        return percentage_missing
    
    def null_counts(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        ''' 
        This method returns a dataframe containing null counts and the percentage of
        nulls in each column. Columns that have no nulls are filterd out
        
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
    
    def get_numeric_columns(self, dataframe: pd.DataFrame, exclude: list[str]=[]) -> list[str]:
        '''
        This method returns a list of columns in a dataframe that are numeric, excluding
        any columns given in the exclude argument 
         
         Parameters:
            dataframe: The required dataframe.
            exclude: columns to remove from the list. Default=None.
        
        Returns:
            A list of numeric columns in the dataframe.
         
         '''
        numeric_columns = dataframe.select_dtypes(include=np.number).columns.tolist()

        if exclude:
            for name in exclude:
                if name in numeric_columns:
                    numeric_columns.remove(name)
                    
        return numeric_columns
