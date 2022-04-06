from enum import unique
from matplotlib.pyplot import get
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

def remove_years(df_pivot, year:int, thresh:float):
    '''
    Remove the first years of the stocks and checks viablility
    '''

    df = get_year(df_pivot)
    df = df[df["Year"].isin(df["Year"].unique()[year:])]

    return get_viable_stocks(df, thresh)


def viable_years(df_pivot, thresh:float):
    df = get_year(df_pivot.isna())

    grouped = df.groupby("Year") 
    
    grouped = grouped.mean()[grouped.mean() < thresh]

    return np.array(grouped.dropna(axis=1).columns)