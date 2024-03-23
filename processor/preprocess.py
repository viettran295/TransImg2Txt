import polars as pl 

def concate_df(dfs: list[pl.DataFrame]) -> pl.DataFrame:
    """
    Vertically concate List of Dataframe
    """
    df_concat = pl.DataFrame()
    for df in dfs:
        df_concat = pl.concat([df_concat, df], how='vertical')
    return df_concat