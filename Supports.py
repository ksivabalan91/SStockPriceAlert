import numpy as np
import yfinance as yf
import pandas as pd
from scipy.signal import find_peaks
from sklearn.cluster import DBSCAN
import Stock as Stock

# Step 1: Identify peaks and troughs
def get_support_resistance_levels(df, distance=5):
    print(f"Identifying support/resistance levels...")
    prices = df['Close'].values.flatten()
    peaks, _ = find_peaks(prices, distance=distance)
    troughs, _ = find_peaks(-prices, distance=distance)
    levels = np.concatenate((prices[peaks], prices[troughs]))
    return levels

# Step 2: Cluster levels to group nearby prices using DBSCAN
def cluster_levels(levels, eps=1.5):
    print(f"Clustering support/resistance levels...")
    levels = np.array(levels).reshape(-1, 1)
    clustering = DBSCAN(eps=eps, min_samples=2).fit(levels)
    clustered_levels = []
    for label in set(clustering.labels_):
        if label == -1:
            continue
        cluster = levels[clustering.labels_ == label]
        clustered_levels.append(cluster.mean())
    return sorted(clustered_levels)

# Step 3: Combine clustering and percentage-based merging
def cluster_levels_combined(levels, percent=1.0):
    print(f"Combining clustered levels with percentage threshold...")
    levels = sorted(levels)
    clustered = []

    for level in levels:
        if not clustered:
            clustered.append([level])
        else:
            last_cluster = clustered[-1]
            representative = sum(last_cluster) / len(last_cluster)
            if abs(level - representative) / representative * 100 <= percent:
                last_cluster.append(level)
            else:
                clustered.append([level])

    # Return average level for each cluster
    merged_levels = [sum(cluster) / len(cluster) for cluster in clustered]
    return merged_levels

def get_supports(stock: Stock):
    print(f"Fetching supports for {stock.ticker}...")
    data_intervals = [stock.daily_hist, stock.weekly_hist, stock.monthly_hist]
    df = pd.DataFrame()
    clustered_levels = []

    for data_interval in data_intervals:
        df = data_interval
        df = df[['Close']].dropna()

        # Dynamically compute clustering parameters
        price_range = df['Close'].max() - df['Close'].min()
        distance = int(len(df) * 0.02)  # 2% of the dataset length
        distance = max(distance, 5)     # Ensure it's not too small
        eps = price_range * 0.02        # 1% of price range

        # Detect and cluster
        levels = get_support_resistance_levels(df, distance=distance)
        get_clustered_levels = cluster_levels(levels, eps=eps)    
        clustered_levels = clustered_levels+get_clustered_levels

    merged_levels = cluster_levels_combined(clustered_levels, percent=5)

    return merged_levels
