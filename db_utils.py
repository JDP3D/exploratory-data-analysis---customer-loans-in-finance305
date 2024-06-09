import yaml
import pandas as pd
from sqlalchemy import create_engine

# Function for credentials
def get_credentials(file_name):
    ''' This function reads a yaml file and returns it's contents'''
    with open(file_name, 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    
    return data

# Function to save data to a csv file

def save_to_csv(loan_dataframe):

    '''This function saves a pandas dataframe to a .csv file'''

    loan_dataframe.to_csv('loan_payments.csv', index=False)




# Class to extract data from RDS database

class RDSDatabaseConnector():

    ''' This class extracts data from a RDS database.'''

    def __init__(self, credentials):
        self.credentials = credentials

    def get_db_connection(self):

        ''' This function establishes a connection withe the remote database using SQLAlchemy'''

        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        ENDPOINT = self.credentials['RDS_HOST']
        USER = self.credentials['RDS_USER']
        PASSWORD = self.credentials['RDS_PASSWORD']
        PORT = self.credentials['RDS_PORT']
        DATABASE = self.credentials['RDS_DATABASE']

        return create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
    
    def get_loan_data(self):

        '''This function extracts the loan data from the RDS database and returns it as a Pandas DataFrame '''

        connection = self.get_db_connection()
        data = pd.read_sql(
        "select * FROM  loan_payments",
        con = connection
        )
        return data

