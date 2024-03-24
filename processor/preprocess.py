import polars as pl 
from utils.error_handler import logger

def concate_df(dfs: list[pl.DataFrame]) -> pl.DataFrame:
    """
    Vertically concate List of Dataframe
    """
    df_concat = pl.DataFrame()
    for df in dfs:
        df_concat = pl.concat([df_concat, df], how='vertical')
    return df_concat

def sum_w_condition(df: pl.DataFrame, sum_col: str, state="Kauf") -> pl.DataFrame:
    """
    Sum vertically with the condition: "State" is equal to "Kauf" or "Verkauf"
    """
    tmp = df.select(
                pl.col(sum_col).filter(pl.col("State") == state).sum()
                )
    df = df.with_columns(
                pl.lit(tmp).alias(f"Sum_{sum_col}_{state}")
                )

    return df
