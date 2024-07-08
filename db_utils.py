from sqlalchemy import create_engine
import pandas as pd
import yaml


# Function for credentials
def get_credentials(file_name: str) -> dict:
    
    ''' 
        This function reads a yaml file and returns it's contents

        parameters:
            file_name (str): Name of yaml file that holds the RDS credentials
        
        returns:
            dict: Dictionary holding the credentials
    '''

    with open(file_name, 'r') as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
    
    return data

# Function to save data to a csv file

def save_to_csv(loan_dataframe: pd.DataFrame) -> None:

    '''
        This function saves a pandas dataframe to a .csv file
    
        parameters:
            loan_dataframe (pandas.DataFrame): The dataframe to write to a csv file
    
    '''

    loan_dataframe.to_csv('loan_payments.csv', index=False)

def csv_to_dataframe(csv_file: str) -> pd.DataFrame:
    
    ''' 
        This function reads a csv file and returns a pandas dataframe
    
        parameters:
            csv_file: The csv_file to convert to a pandas DataFrame
        
        return:
            pd.DataFrame
    '''

    data = pd.read_csv(csv_file)

    return data



# Class to extract data from RDS database

class RDSDatabaseConnector:

    ''' 
        This class consists of functions to extract and write data from a RDS database.

        Attributes: 
            PRIVATE
    
    '''

    def __init__(self, credentials):
        self.__credentials = credentials

    def __get_database_connection(self):

        ''' This function establishes a connection with the remote database using SQLAlchemy'''

        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        ENDPOINT = self.__credentials['RDS_HOST']
        USER = self.__credentials['RDS_USER']
        PASSWORD = self.__credentials['RDS_PASSWORD']
        PORT = self.__credentials['RDS_PORT']
        DATABASE = self.__credentials['RDS_DATABASE']

        return create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
    
    def get_loan_data(self):

        '''This function extracts the loan data from the RDS database and returns it as a Pandas DataFrame '''

        connection = self.__get_database_connection()
        data = pd.read_sql(
        "select * FROM  loan_payments",
        con = connection
        )
        return data

# run script to retrieve database and write it to a local csv file
if __name__ == "__main__":
    
    credentials = get_credentials('C:/Users/JS/Documents/AiCore/Projects/EDA/credentials.yaml')

    data = RDSDatabaseConnector(credentials).get_loan_data()
    
    save_to_csv(data)
