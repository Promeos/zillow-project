import pandas as pd
import env
import os


def get_connection(db, user=env.user, host=env.host, password=env.password):
    '''
    Returns a formatted url with login credentials to access data stored in a SQL data warehouse.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'


def get_zillow_data():
    '''
    Acquires a zillow dataset from a SQL Database and returns it as a pandas dataframe.
    
    If the dataset is not stored in your cache, a local copy will be made.
    '''
    
    db = 'zillow'
    
    sql_query = '''
    WITH pred2017 AS (
    SELECT parcelid AS parcel_id,
        LAST_VALUE(logerror)
            OVER (PARTITION BY parcelid ORDER BY transactiondate
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS log_error,
        LAST_VALUE(transactiondate)
            OVER (PARTITION BY parcelid ORDER BY transactiondate
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS transaction_date
    FROM predictions_2017
    WHERE transactiondate BETWEEN '2017-05-01' AND '2017-07-31'
    ORDER BY id, parcelid)

    SELECT id,
        transaction_date,
        parcel_id,
        bathroomcnt AS baths,
        bedroomcnt AS beds,
        finishedsquarefeet12 AS sqft,
        lotsizesquarefeet AS lot_sqft,
        fips,
        latitude,
        longitude,
        regionidzip AS region_zip_id,
        yearbuilt AS year_built,
        landtaxvaluedollarcnt AS land_tax_value,
        taxamount AS tax_amount,
        log_error
    FROM properties_2017 AS p1
    INNER JOIN pred2017 AS p2
    ON p1.parcelid = p2.parcel_id
    WHERE propertylandusetypeid IN (261, 262, 273)
    ORDER BY id, parcelid;
    '''
        
    filename = './data/raw/zillow.csv'
    
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        df = pd.read_sql(sql_query, get_connection(db))
        df.to_csv(filename, index=False)
        return df
