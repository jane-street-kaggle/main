import numpy as np
import polars as pl

def reduce_memory(df: pl.DataFrame) -> pl.DataFrame:
    """Optimize data types for memory usage in Polars"""
    start_mem = df.estimated_size() / (1024**2)
    print(f'Memory usage of dataframe is {start_mem:.2f} MB')
    
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type in [pl.Float64, pl.Float32, pl.Int64, pl.Int32, pl.Int16, pl.Int8]:
            c_min = df[col].drop_nulls().min()
            c_max = df[col].drop_nulls().max()
            
            if c_min is not None and c_max is not None:  # null check 추가
                if col_type in [pl.Int64, pl.Int32, pl.Int16, pl.Int8]:
                    if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max: # type: ignore  # noqa: E501
                        df = df.with_columns(pl.col(col).cast(pl.Int8))
                    elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max: # type: ignore  # noqa: E501
                        df = df.with_columns(pl.col(col).cast(pl.Int16))
                    elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max: # type: ignore  # noqa: E501
                        df = df.with_columns(pl.col(col).cast(pl.Int32))
                    elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max: # type: ignore  # noqa: E501
                        df = df.with_columns(pl.col(col).cast(pl.Int64))
                else:
                    if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                        df = df.with_columns(pl.col(col).cast(pl.Float32))
                    else:
                        df = df.with_columns(pl.col(col).cast(pl.Float64))
        
        elif col_type == pl.Utf8:
            df = df.with_columns(pl.col(col).cast(pl.Categorical))
    
    end_mem = df.estimated_size() / (1024**2)
    print(f'Memory usage after optimization is: {end_mem:.2f} MB')
    print(f'Decreased by {100 * (start_mem - end_mem) / start_mem:.1f}%')
    
    return df
