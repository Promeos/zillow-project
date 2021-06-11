import pandas as pd
import env
import os


def get_connection(db, user=env.user, host=env.host, password=env.password):
    '''
    Returns a formatted url with login credentials to access data on a SQL database.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def load_zillow_data():
    '''
    This function acquires the zillow dataset from a SQL Database.
    It returns the zillow dataset as a Pandas DataFrame.
    
    A local copy will be created as a csv file in the current directory for future use.
    '''
    db = 'zillow'
    sql_query = '''
        select *
        from properties_2017
        join predictions_2017 as pred using(parcelid)
        where pred.transactiondate between '2017-05-01' and '2017-06-30';
        '''
    file = 'zillow.csv'
    
    if os.path.isfile(file):
        return pd.read_csv('zillow.csv')
    else:
        df = pd.read_sql(sql_query, get_connection(db))
        df.to_csv('zillow.csv', index=False)
        return df
