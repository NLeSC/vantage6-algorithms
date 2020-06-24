import os

import pandas as pd
import sparql
from vantage6.tools.util import info


def RPC_column_names(data: pd.DataFrame, *args, **kwargs):
    """Column names

    List the names of the table columns
    """
    info("Retrieving column names")

    # what you return here is sent to the central server. So make sure
    # no privacy sensitive data is shared
    return data.columns.to_list()


def RPC_correlation_matrix(data: pd.DataFrame, *args, **kwargs):
    return data.corr()


def RPC_get_data(data: pd.DataFrame, *args, **kwargs):
    """
    Return the raw data.
    TODO: This function should not exist in the final version of the code! The data should be pseudonymized at the very
        least!

    """
    return data


def RPC_sample_sparqle_query(data: None, *args, **kwargs):
    """
    Get the transactions that where processed by server A (example query on toy
    transactions dataset)
    """
    database_uri = os.environ["DATABASE_URI"]
    # database_uri is prepended with the data folder in the vantage6 node setup.
    # therefore we need to extract the actual database_uri for our db endpoint
    endpoint = database_uri[database_uri.find('http'):]
    q = '''
    PREFIX log: <http://example.org/ont/transaction-log/>
    PREFIX srv: <http://example.org/data/server/>

        SELECT ?transaction where {
            ?transaction log:processedBy srv:A
        } limit 10
    '''
    print(f'Trying to send query to {endpoint}')
    result = sparql.query(endpoint, q)
    return [row[0] for row in result]
