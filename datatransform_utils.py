import pandas as pd

#Class for converting data

class DataTransform:

    def to_float64(self, dataframe: pd.DataFrame, column: str | list[str]) -> pd.Series | pd.DataFrame:
        '''
        This method is used to convert column(s) data type to float64.

        Parameters:
            dataframe: The dataframe to which this method will be applied.
            columns: The name(s) of columns that contains the data to be converted.

        Returns:
            series or dataFrame: The series/dataframe with converted data type.
        '''
        return dataframe[column].astype('float64')
    
    def to_categorical(self, dataframe: pd.DataFrame, column: str | list[str]) -> pd.Series | pd.DataFrame:
        '''
        This method is used to convert column(s) data type to categorical.

        Parameters:
            dataframe: The dataframe to which this method will be applied.
            columns: The name(s) of columns that contains the data to be converted.

        Returns:
            series or dataFrame: The series/dataframe with converted data type.
        '''
        return dataframe[column].astype('category')

    def to_int64(self, dataframe: pd.DataFrame, column: str | list[str]) -> pd.Series | pd.DataFrame:
        '''
        This method is used to convert column(s) data type to int64.

        Parameters:
            dataframe: The dataframe to which this method will be applied.
            column: The name(s) of columns that contains the data to be converted.

        Returns:
            series or dataFrame: The series/dataframe with converted data type.
        '''
        return  dataframe[column].astype('int64')

    def to_datetime(self, dataframe, column, date_format):
        '''
        This method is used to convert column(s) data type to datetime.

        Parameters:
            dataframe: The dataframe to which this method will be applied.
            columns: Thee name(s) of columns that contains the data to be converted.
            date_format: The date format that the original data is in.

        Returns:
            dataframe: The updated dataframe.
        '''
        return pd.to_datetime(dataframe[column], format = date_format)
    
    def to_string(self, dataframe: pd.DataFrame, column: str | list[str]) -> pd.Series | pd.DataFrame:
        '''
        This method is used to convert column(s) data type to str.

        Parameters:
            dataframe: The dataframe to which this method will be applied.
            columns: The name(s) of columns that contains the data to be converted.

        Returns:
            series or dataFrame: The series/dataframe with converted data type.
        '''

        return dataframe[column].astype('string')
    
    def string_replace(self, dataframe: pd.DataFrame, column: str, old: str, new:str, regex: bool=False) -> pd.Series:
        '''
        This method is to replace a string or parts of a string with a new string.

        Parameters:
            dataframe: The dataframe to which this method will be applied.
            column: The name of the column that contains the data to be converted.
            old: The original string to be replaced/amended
            new: The new string/amendments

        Returns:
            Series: The updated series.
        '''
        return dataframe[column].str.replace(old, new, regex=regex)
    