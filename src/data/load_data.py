import os
import pandas as pd

def load_data():
    """
    Loads Twitter_Data.csv and Reddit_Data.csv, standardizes column names,
    and returns a combined DataFrame with 'text' and 'sentiment'.
    """
    # Check if files are in data/ or data/raw/
    base_dir = os.path.join("data", "raw") if os.path.exists(os.path.join("data", "raw")) else "data"
    
    twitter_path = os.path.join(base_dir, "Twitter_Data.csv")
    reddit_path = os.path.join(base_dir, "Reddit_Data.csv")
    
    dfs = []
    
    if os.path.exists(twitter_path):
        df_tw = pd.read_csv(twitter_path)
        # Standardize column names
        df_tw = df_tw.rename(columns={'clean_text': 'text', 'category': 'sentiment'})
        dfs.append(df_tw[['text', 'sentiment']])
        print(f"Loaded {len(df_tw)} rows from Twitter dataset.")
        
    if os.path.exists(reddit_path):
        df_rd = pd.read_csv(reddit_path)
        # Standardize column names
        df_rd = df_rd.rename(columns={'clean_comment': 'text', 'category': 'sentiment'})
        dfs.append(df_rd[['text', 'sentiment']])
        print(f"Loaded {len(df_rd)} rows from Reddit dataset.")
        
    if not dfs:
        raise FileNotFoundError("Could not find Twitter_Data.csv or Reddit_Data.csv in 'data/' or 'data/raw/'!")
        
    combined_df = pd.concat(dfs, ignore_index=True)
    print(f"✅ Total combined records: {len(combined_df)}")
    return combined_df

if __name__ == "__main__":
    df = load_data()
    print(df.head())