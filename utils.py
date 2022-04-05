import pandas as pd
import numpy as np



## Helper functions to deal with NA's




def get_viable_stocks(df_pivot, thresh:float):
    '''
    Returns an array of stocks that have less NaN's than a certain threshold
    '''
    df_isnull = df_pivot.isnull()

    indexes = df_isnull.mean()[df_isnull.mean() < thresh].index

    return np.array(indexes)

def index_to_datetime(df_pivot):
    df_pivot.index = pd.to_datetime(df_pivot.index)
    return df_pivot


def get_year(df_pivot):
    '''
    Returns a pd.dataframe with a new column for the years called "year"
    '''
    df = index_to_datetime(df_pivot)

    df["Year"] = df.index.year

    return df
