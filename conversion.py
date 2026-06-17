import pandas as pd


def dtype_conversion(df):

    for col in df.columns:

        if df[col].dtypes == "object":
            try:
                df[col]=pd.to_numeric(df[col])
  
            except:

                try:
                    df[col]=pd.to_datetime(df[col])
            
                except:

                    pass
    
    
    return df


    

