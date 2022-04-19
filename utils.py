from enum import unique
import matplotlib.pyplot as plt
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
    '''
    Returns stocks where for every year, the amout of NA's doesn't exceed the threshold
    '''

    df = get_year(df_pivot.isna())

    grouped = df.groupby("Year") 
    
    grouped = grouped.mean()[grouped.mean() < thresh]

    return np.array(grouped.dropna(axis=1).columns)

def get_weekly_stocks(df_pivot, tolerance:int):
    df = get_year(df_pivot.isna())
    df["Week"] = df.index.isocalendar().week

    grouped = df.groupby(["Year", "Week"])
    grouped = grouped.sum()
    final = grouped <= tolerance
    
    return final.sum(axis = 1)

def plothist(df_pivot, thresh:int):
    fig, ax = plt.subplots(3,2, sharex = True, sharey = True, tight_layout = True)
    zero = get_weekly_stocks(df_pivot, 0)
    one = get_weekly_stocks(df_pivot, 1)
    two = get_weekly_stocks(df_pivot, 2)
    three = get_weekly_stocks(df_pivot, 3)
    four = get_weekly_stocks(df_pivot, 4)
    five = get_weekly_stocks(df_pivot, 5)


    ax[0,0].hist(zero)
    ax[0,1].hist(one)
    ax[1,0].hist(two)
    ax[1,1].hist(three)
    ax[2,0].hist(four)
    ax[2,1].hist(five)
    ax[0,0].vlines(thresh,0, 400, linestyles = "dashed", color = "r", label = "80")
    ax[0,1].vlines(thresh, 0, 400, linestyles = "dashed", color = "r",label = "80")
    ax[1,0].vlines(thresh, 0, 400, linestyles = "dashed", color = "r", label = "80")
    ax[1,1].vlines(thresh, 0, 400, linestyles = "dashed", color = "r", label = "80")
    ax[2,0].vlines(thresh, 0, 400, linestyles = "dashed", color = "r", label = "80")
    ax[2,1].vlines(thresh, 0, 400, linestyles = "dashed", color = "r", label = "80")


    ax[0,0].set_ylabel("Count")
    ax[1,0].set_ylabel("Count")
    ax[2,0].set_ylabel("Count")
    ax[2,0].set_xlabel("Number of viable stocks per week")
    ax[2,1].set_xlabel("Number of viable stocks per week")

    ax[0,0].set_title("0 missing values a week")
    ax[0,1].set_title("=<1 missing value a week")
    ax[1,0].set_title("=<2 missing values a week")
    ax[1,1].set_title("=<3 missing values a week")
    ax[2,0].set_title("=<4 missing values a week")
    ax[2,1].set_title("=<5 missing values a week")
    return plt.show()

def percent_above(df_pivot, thresh:int):
    for i in [0,1,2,3,4,5]:
        x = get_weekly_stocks(df_pivot, i) > thresh
        x = x.mean()*100
        print("If we allow " + str(i) + " or less NaN's we get " + str(x) + " percent of weeks with more than " + str(thresh) + " viable stocks")
    return 