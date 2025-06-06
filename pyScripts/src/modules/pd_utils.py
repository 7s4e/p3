"""
Pandas Utilities Module

This module provides utility functions for data processing and 
transformation with pandas.
"""
# Standard library imports
from io import StringIO
from pandas import DataFrame, Timestamp
from pandas.tseries.offsets import DateOffset, BDay
from typing import Any, Union
import pandas as pd

# Local module imports
from .constants import DATE_FORMATS


def cast_as_string(df: DataFrame, raw_columns: list[str]) -> DataFrame:
    """
    Casts specified columns in a DataFrame to the pandas 'string' dtype,
    replacing missing values (NaNs) with Python None for consistency.

    Args:
        df (DataFrame): The input pandas DataFrame.
        raw_columns (list[str]): A list of column names in `df` to cast as 
            strings.

    Returns:
        DataFrame: A new DataFrame with the specified columns cast to 
        the 'string' dtype, and missing values replaced with None.
    """
    formatted_columns = {}

    for col in raw_columns:
        series = df[col].where(df[col].notna(), None).astype("string") 

        # Remove Excel-style formula wrapper
        if series.dropna().str.match(r'^=".*"$').any():
            series = series.str.extract(r'^="(.*?)"$')[0]
        
        formatted_columns[col] = series

    return df.assign(**formatted_columns)


def convert_to_number(df: DataFrame, cols: list[str]) -> DataFrame:
    """
    Converts specified columns in a DataFrame to numeric dtype, coercing 
    invalid parsing to NaN.

    Args:
        df (DataFrame): The input pandas DataFrame.
        cols (list[str]): A list of column names in `df` to convert 
            to numeric types.

    Returns:
        DataFrame: A new DataFrame with the specified columns converted 
        to numeric types. Non-numeric values are replaced with NaN.
    """
    return df.assign(**{col: pd.to_numeric(df[col], errors='coerce')
                        for col in cols})


def ensure_column(df: DataFrame, header: str, value: Any) -> DataFrame:
    if header not in df.columns:
        df[header] = value
    return df


def format_dates(df: DataFrame, cols: list[str], date_frmt: str = ""
                 ) -> DataFrame:
    """
    Converts specified DataFrame columns to datetime using a given 
        format.

    Args:
        df (DataFrame): The input pandas DataFrame.
        cols (list[str]): A list of column names in `df` to convert to 
            datetime.
        date_frmt (str, optional): A string key representing the date 
            format, as defined in the `DATE_FORMATS` dictionary. If not 
            provided or not found, pandas will infer the format.

    Returns:
        DataFrame: A new DataFrame with the specified columns converted to 
        datetime. Invalid parsing results in NaT.
    """
    format_str = DATE_FORMATS.get(date_frmt.lower(), None)
    return df.assign(**{
        col: pd.to_datetime(df[col], format=format_str or None, 
                            errors="coerce") 
        if col in df.columns else pd.NaT
        for col in cols
    })


def offset_date(ref_date: Timestamp, yrs: int = 0, mos: int = 0, dys: int = 0, 
                biz_dys: int = 0) -> Timestamp:
    """
    Returns a new date offset from the reference date by a specified 
    number of years, months, days, or business days.

    Only one type of offset is applied: if `biz_dys` is non-zero, 
    business day offset is used and the year/month/day values are 
    ignored. Otherwise, calendar-based offset is used.

    Args:
        ref_date (Timestamp): The reference date to offset from.
        yrs (int, optional): Number of calendar years to add/subtract.
        mos (int, optional): Number of calendar months to add/subtract.
        dys (int, optional): Number of calendar days to add/subtract.
        biz_dys (int, optional): Number of business days to add/subtract.
            Takes precedence over calendar-based offsets.

    Returns:
        Timestamp: The resulting date after applying the offset.
    """
    offset = (BDay(biz_dys) if biz_dys 
              else DateOffset(years=yrs, months=mos, days=dys))
    return ref_date + offset


def read_csv(file_path: str, sep: str = ",", header: int = 0) -> DataFrame:
    """
    Reads a CSV file into a pandas DataFrame with common NA value 
    handling.

    Args:
        file_path (str): Path to the CSV file.
        sep (str, optional): Delimiter to use. Defaults to ",".
        header (int, optional): Row number to use as the column names. 
            Defaults to 0.

    Returns:
        DataFrame: A pandas DataFrame containing the data from the CSV 
        file, with specified NA values parsed as missing.
    """
    return pd.read_csv(file_path, sep=sep, header=header, 
                       na_values=["", " ", "NA", "N/A", "null", "None", "--"],
                       keep_default_na=True, encoding='utf-8')


def read_csv_until_blank_line(file_path: str) -> DataFrame:
    """
    Reads a CSV file up to the first blank line and returns the content 
    as a DataFrame.

    This function reads a CSV file line by line and stops reading once 
    it encounters a completely blank line. The data before that line is 
    then parsed into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        DataFrame: A pandas DataFrame containing the data up to the 
        first blank line.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        buffer = []
        for line in file:
            if line.strip() == "":
                break
            buffer.append(line)
    return read_csv(StringIO(''.join(buffer)))


def split_columns(df: DataFrame, src_col: str, dest_cols: tuple[str, ...], 
                  regex_pattern: str, dtype: Union[type, str], 
                  drop_src: bool = True) -> DataFrame:
    """
    Splits a single source column into multiple destination columns by 
    extracting substrings using a regular expression pattern.

    Args:
        df (DataFrame): The input DataFrame.
        src_col (str): The name of the source column to split.
        dest_cols (tuple[str, ...]): A tuple of destination column names 
            to create.
        regex_pattern (str): A regex pattern with capturing groups to 
            extract parts of the source column's string values.
        dtype (Union[type, str]): The data type to which the extracted 
            columns should be cast.
        drop_src (bool, optional): Whether to drop the source column 
            from the returned DataFrame. Defaults to True.

    Returns:
        DataFrame: A DataFrame with the extracted columns added, and optionally the 
            source column dropped.
    """
    # print(f"LOG: split_columns() start")
    extraction = df[src_col].str.extract(regex_pattern, expand=True)
    # print(f"LOG: exraction = {extraction}")
    # df[list(dest_cols)] = extraction.astype(dtype)
    # return df.drop(columns=[src_col]) if drop_src else df
    for col in extraction.columns:
        extraction[col] = extraction[col].str.replace(",", "", regex=False)
        extraction[col] = extraction[col].astype(dtype)
    df[list(dest_cols)] = extraction
    # print(f"LOG: split_columns() end")
    return df.drop(columns=[src_col]) if drop_src else df


def stack_dataframes():
    pd.concat()