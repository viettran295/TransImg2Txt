import re 
import polars as pl
from utils.error_handler import logger

def exclude_number(s: str) -> str:
    """
    Exclude numbers in string
    """
    numbers = re.findall(r'\d+', s)
    for num in numbers:
        s = s.replace(num, '')
    return s 

def extract_name(s: str) -> str:
    """
    Extract file name from path (e.g ./img/name1.png)
    """
    name_wExt = s.split('/')[-1].split('.')[0]
    return exclude_number(name_wExt)

def str_to_number(df: pl.DataFrame, cols: str, type: pl.DataType) -> pl.DataFrame:
    """
    Convert columns from string to decimal in a List of Dataframe
    """
    try:
        # Extract numbers by regex
        df = df.with_columns(
                    pl.col(cols).str.extract_all(r"\d+([\.]\d+)?*([\,]\d+)?").explode()
                    )
        # Replace ',' to '.' or '.' to ''
        df = df.with_columns(
                    pl.col(cols).str.replace(r"\.", "")
                    )
        df = df.with_columns(
                    pl.col(cols).str.replace(r"\,", ".")
                    )
        # Cast string to float64
        df = df.with_columns(
                    pl.col(cols).cast(type)
                    )
    except Exception as ex:
        logger.error(f"Error while converting -> {ex}")

    return df