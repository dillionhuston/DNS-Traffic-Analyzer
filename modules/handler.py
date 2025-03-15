import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import time

dns_traffic_data = "data.xlsx"

st.title("DNS TRAFFIC STATS")

domain_chart = st.empty()
ip_chart = st.empty()
traffic_chart = st.empty()

def get_data():
    try:
        df = pd.read_excel(dns_traffic_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        st.error(f"Error reading the data: {e}")
        return pd.DataFrame()

def update_charts(df):
    domain_counts = df['query_name'].value_counts().nlargest(10)
    domain_fig = go.Figure(data=[go.Bar(x=domain_counts.index, y=domain_counts.values)])
    domain_fig.update_layout(title="Top 10 Queried Domains", xaxis_title="Domain", yaxis_title="Count")
    domain_chart.plotly_chart(domain_fig, use_container_width=True, key="domain_chart")

    ip_counts = df['source_ip'].value_counts().nlargest(10)
    ip_fig = go.Figure(data=[go.Bar(x=ip_counts.index, y=ip_counts.values)])
    ip_fig.update_layout(title="Top 10 Source IPs", xaxis_title="IP", yaxis_title="Count")
    ip_chart.plotly_chart(ip_fig, use_container_width=True, key="ip_chart")

    traffic_counts = df.groupby(pd.Grouper(key='timestamp', freq='10S')).size()
    traffic_fig = go.Figure(data=[go.Scatter(x=traffic_counts.index, y=traffic_counts.values, mode='lines+markers')])
    traffic_fig.update_layout(title="DNS Traffic Over Time", xaxis_title="Timestamp", yaxis_title="Query Count")
    traffic_chart.plotly_chart(traffic_fig, use_container_width=True, key="traffic_chart")

while True:
    df = get_data()
    if not df.empty:
        update_charts(df)
    time.sleep(10)