import pandas as pd
import matplotlib.pyplot as plt

dns_traffic_data = "data.xlsx"


def TrafficCounts():

    df = pd.read_excel(dns_traffic_data)
    expected_columns = ["timestamp", "source_ip", "dst_ip", "query_name", "query_type"]

    if not all(col in df.columns for col in expected_columns):
        print("error reading")
        return None, None, None  

    domain_counts = df["query_name"].value_counts().nlargest(10)
    ip_counts = df["source_ip"].value_counts().nlargest(10)
    query_type_counts = df["query_type"].value_counts().nlargest(10)
    print("read excel")
    
    # make sure its not empty
    return domain_counts, ip_counts, query_type_counts

def plotgraph(domain_counts, ip_counts, query_type_counts):
    if domain_counts is None or ip_counts is None or query_type_counts is None:
        print("no data to plot")
        return

    if not domain_counts.empty:
        plt.figure(figsize=(10, 5))
        domain_counts.plot(kind="bar", title="top ten domain names")
        plt.xticks(rotation=180)
        plt.xlabel("Domains")
        plt.ylabel("Query Count")
        
        plt.show()

    if not ip_counts.empty:
        plt.figure(figsize=(10, 5))
        ip_counts.plot(kind="bar", title="top ten ip sources")
        plt.xticks(rotation= 45)
        plt.xlabel("Source IPs")
        plt.ylabel("Query Count")
        plt.show()

    if not query_type_counts.empty:
        plt.figure(figsize=(10, 5))
        query_type_counts.plot(kind="bar", title="top ten query types")
        plt.xlabel("Query Type")
        plt.ylabel("Count")
        plt.show()


domain_counts, ip_counts, query_type_counts = TrafficCounts()

# Plot the graphs only if data exists
if domain_counts is not None and ip_counts is not None and query_type_counts is not None:
    plotgraph(domain_counts, ip_counts, query_type_counts)