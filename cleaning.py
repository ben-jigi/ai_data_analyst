import os
import pandas
import numpy

def basic_cleaning(df):

    df.columns=(
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ","_")
    )

    df=df.drop_duplicates()
    df=df.dropna(how="all")
    df=df.dropna(axis=1,how="all")

    for col in df.select_dtypes(include="object").columns:
        df[col]=df[col].str.strip()

    return df

def fill_mean(df, column):

    df[column] = df[column].fillna(
        df[column].mean()
    )

    return df

def fill_median(df, column):

    df[column] = df[column].fillna(
        df[column].median()
    )

    return df

def fill_mode(df, column):

    df[column] = df[column].fillna(
        df[column].mode()[0]
    )

    return df


def drop_constant_columns(df):

    constant_columns = []

    for col in df.columns:

        if df[col].nunique() == 1:

            constant_columns.append(col)

    return df.drop(
        columns=constant_columns
    )

def detect_id_columns(df):

    id_columns = []

    for col in df.columns:

        if df[col].nunique() == len(df):

            id_columns.append(col)

    return id_columns

def drop_columns(df, columns):

    return df.drop(
        columns=columns
    )

def detect_outliers_iqr(
    df,
    column
):

    q1 = df[column].quantile(0.25)

    q3 = df[column].quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr

    upper = q3 + 1.5 * iqr

    mask=(df[column] < lower)|(df[column] > upper)
    
    percentage = (
        mask.sum() / len(df)
    ) * 100

    if percentage <= 15:
        return "REMOVABLE"

    else:

        return "MANUAL_REVIEW"
    
    
def remove_outliers_iqr(
    df,
    column
):

    q1 = df[column].quantile(0.25)

    q3 = df[column].quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr

    upper = q3 + 1.5 * iqr

    return df[
        (df[column] >= lower)
        &
        (df[column] <= upper)
    ]
