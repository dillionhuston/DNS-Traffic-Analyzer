import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import time

# Path to your Excel file
dns_traffic_data = "data.xlsx"

# Title of the app
st.title("DNS TRAFFIC STATS")

# Placeholder for the plotly graphs
domain_graph_placeholder = st.empty()
ip_graph_placeholder = st.empty()
query_type_graph_placeholder = st.empty()

# Function to get data and update the graph
def get_data():
    try:
        df = pd.read_excel(dns_traffic_data)  
        domain_counts = df['query_name'].value_counts().nlargest(10)
        ip_counts = df['source_ip'].value_counts().nlargest(10)
        dns_query_types = df['query_type'].value_counts().nlargest(10)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # domain bar
        domain_fig = go.Figure(data=[go.Bar(x=domain_counts.index, y=domain_counts.values)])
        domain_fig.update_layout(title="Top 10 Queried Domains", xaxis_title="Domain", yaxis_title="Count")
        
        # ip bar
        ip_fig = go.Figure(data=[go.Bar(x=ip_counts.index, y=ip_counts.values)])
        ip_fig.update_layout(title="Top 10 Source IPs", xaxis_title="IP", yaxis_title="Count")

     
        traffic_counts = df.groupby(pd.Grouper(key='timestamp', freq='10S')).size()

       
        traffic_spikes = traffic_counts[traffic_counts > traffic_counts.quantile(0.95)]  
        spikes = go.Figure()

        spikes.add_trace(go.Scatter(x=traffic_counts.index, y=traffic_counts.values, mode='lines', name="Traffic"))

      
        spikes.add_trace(go.Scatter(x=traffic_spikes.index, y=traffic_spikes.values, mode='markers', name="Spikes", marker=dict(color='red', size=10)))
        spikes.update_layout(title="DNS Traffic with Spikes", xaxis_title="Timestamp", yaxis_title="Traffic Count", showlegend=True)

        return domain_fig, ip_fig, spikes

    except Exception as e:
        st.error(f"Error reading the data: {e}")
        return go.Figure(), go.Figure(), go.Figure()


while True:
    domain_fig, ip_fig, spikes = get_data()

    domain_graph_placeholder.plotly_chart(domain_fig, use_container_width=True)
    ip_graph_placeholder.plotly_chart(ip_fig, use_container_width=True)
    query_type_graph_placeholder.plotly_chart(spikes, use_container_width=True)

    time.sleep(10)  
