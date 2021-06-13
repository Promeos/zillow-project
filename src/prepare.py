import pandas as pd
import os

from sklearn.model_selection import train_test_split


def prepare_zillow(data):
    '''
    Signature: prepare_zillow(data) -> pandas.core.frame.DataFrame
    Docstring:
    Prepare the zillow dataset for data EDA
    Return DataFrame of zillow dataset
    Parameters
    ----------
    data : pandas.core.frame.DataFrame
    data is the Zillow dataset stored as `zillow.csv`
    Returns
    -------
    DataFrame of the zillow dataset
    Examples
    --------
    '''
    filename = "./data/prepared/zillow_prep.csv"
    
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        data = data.drop_duplicates().dropna() 
        numeric_cols = ['fips', 'region_zip_id', 'year_built']
        data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, downcast='integer')
        data.latitude = data.latitude.astype('int').astype('str').apply(normalize_coordinates, index=2).astype('float')
        data.longitude = data.longitude.astype('int').astype('str').apply(normalize_coordinates, index=4).astype('float')
        data.to_csv(filename, index=False)
        return data
 
 
def normalize_coordinates(geopoint, index):
    '''
    Insert a period (.) in latitude and longitude values for plotting.
    '''
    return geopoint[:index] + '.' + geopoint[index:]   
    

def create_datasets(dataset):
    '''
    Splits the zillow dataset into train, validate, and test sets.
    
    Data splits = 70%-20%-10%
    
    Parameters
    ----------
    dataset :
        The zillow dataset returned by the `prepare_zillow` function
    
    Returns
    -------
    train, validate, test

    '''
    # Split the dataset into train, and validation + test sets
    train, validate_test = train_test_split(dataset,
                                            test_size=.3,
                                            random_state=369)

    # Split validate_test portion into validate and test sets
    validate, test = train_test_split(validate_test,
                                      test_size=.33,
                                      random_state=369)

    return train, validate, test


def create_X_y_sets(train, validate, test):
    '''
    Removes all non-numeric columns from the train, validate, and test datasets.
    Dataset are split into X and y dataframes for data modeling.

    Parameters
    ----------
    train, validate, test
    
    Returns
    -------
    X_train, y_train, X_validate, y_validate, X_test, y_test
    '''
    # Create a variable to store the target name to the list of columns dropped from
    # the X datasets
    TARGET = 'log_error'

    # Create a list of nonnumeric columns to remove from the dataset.
    columns_to_drop = list(train.select_dtypes(exclude='number').columns)
    columns_to_drop.append(TARGET)

    # Automate data splitting using python's built-in exec() function.
    for dataset in ['train', 'validate', 'test']:
        exec(f'X_{dataset}={dataset}.drop(columns=columns_to_drop)')
        exec(f'y_{dataset}={dataset}[[TARGET]]')

    return X_train, y_train, X_validate, y_validate, X_test, y_test