# Project Title: Exploratory Data Analysis - Customer Loans in Finance
### Project description:  
This project is for a data analysis course that I am currently taking. The goal of the project is to clean and analyse data from a loans database.
### Installation instructions: 
1. Clone the repository: 

       git clone https://github.com/JDP3D/exploratory-data-analysis---customer-loans-in-finance305.git

2. Install dependencies:  
The project was created with python 3.10.14.

        pip install the following libraries:
        
        matplotlib 
        missingno
        numpy
        pandas
        scipy
        seaborn
        scipy
        sqlalchemy
        statsmodels
        yaml



### Usage Instructions:  
Run the code in the jupyter notebooks milestone_03ipynb and milestone_04.ipynb. The databases will be loaded from the provided csv files. 

### Project file structure
- db_utils: utilities for fetching and outputting the database. Running this script will download the database and write it to a local csv file named loan_payments.csv. Please note that you will not be able to access the remote database, csv copies have been provided.
  
- milestone_02.ipynb: A jupyter notebook that can be used to chack the database (Project Task 3 of milestone 2)

- dataframe_info.py: utlities for extracting statistical other information of interest from a pandas dataframe dataframe .

- dataframe_utils.py: Utilities useful for cleaning and transforming the database.

- datatransform_utils.py: Utilities used to convert data types.

- milestone_03.ipynb: A Jupyter notebooked used to explore, clean and transform the database.

- milestone_04.ipynb: A Jupyter notebook used to analyse and visualise diferent aspects of the database.

- loan_payments.csv: The raw uncleaned database.

- cleaned_loan_data.csv: The cleaned untransformed database

- transformed_loan_data.csv: The transformed database.


### Licence  

The program is in the public domain, you may do with it as you will.