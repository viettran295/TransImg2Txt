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
    if "State" in df.columns:
        tmp = df.select(
                    pl.col(sum_col).filter(pl.col("State") == state).sum()
                    )
        df = df.with_columns(
                    pl.lit(tmp).alias(f"Sum_{sum_col}_{state}")
                    )
    else: 
        logger.exception("Error while operating function sum --> Column does not exist")

    return df

def profit_and_loss(df: pl.DataFrame) -> pl.DataFrame:
    """
    Calculate profit and loss 
    """
    if "Sum_Price_Kauf" in df.columns and "Sum_Amount_Verkauf" in df.columns:
        df = df.with_columns(
                    (pl.col("Sum_Price_Kauf") / pl.col("Sum_Amount_Kauf"))
                    .alias("Avg_Price_Buy")
                    )
        df = df.with_columns(
                    (pl.col("Sum_Price_Verkauf") / pl.col("Sum_Amount_Verkauf"))
                    .alias("Avg_Price_Sell")
                    )
        df = df.with_columns(
                    ((pl.col("Avg_Price_Sell") - pl.col("Avg_Price_Buy")) / pl.col("Avg_Price_Buy") * 100)
                    .alias("Profit%")
                    )
    return df