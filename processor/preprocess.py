import polars as pl 
from utils.error_handler import logger
import yfinance as yf

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
    Calculate :
        - Average buying and selling price
        - Profit and loss in %
        - Current profit and loss in % when compare with curren market price
    """
    if "Sum_Price_Kauf" in df.columns and "Sum_Amount_Verkauf" in df.columns \
        and "Market_Price" in df.columns:
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
        df = df.with_columns(
                    ((pl.col("Market_Price") - pl.col("Avg_Price_Buy")) / pl.col("Avg_Price_Buy") * 100)
                    .alias("Current_Profit%")
                    )
    else:
        logger.exception("Error while operating function sum --> Column does not exist")
    return df

def add_market_price(df: pl.DataFrame, ticker: str) -> pl.DataFrame:
    """
    Add current market price to Dataframe
    """
    ticker = ticker.upper()
    price = yf.Ticker(ticker).info['dayHigh']
    return df.with_columns(
                    pl.lit(price).alias("Market_Price")
                )