import pandas as pd

class DataTransform:

    def to_float64(self, dataframe, column):
        return dataframe[column].astype('float64')
    
    def to_categorical(self, dataframe, column):
        return dataframe[column].astype('category')

    def to_int64(self, dataframe, column):
        return  dataframe[column].astype('int64')

    def to_datetime(self, dataframe, column, date_format):
        return pd.to_datetime(dataframe[column], format = date_format)
    
    def to_string(self, dataframe, column):
        return dataframe[column].astype('string')
    
    def string_replace(self, dataframe, column, old, new, regex=False):
        return dataframe[column].str.replace(old, new, regex=regex)
    