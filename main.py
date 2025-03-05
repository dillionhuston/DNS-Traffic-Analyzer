import pandas as pd
from scapy.all import DNS, DNSQR, IP, sniff
from openpyxl import Workbook as op
from openpyxl import load_workbook
from datetime import datetime
from modules.test_module import graph
from modules.handler import TrafficCounts, plotgraph


dns_traffic_data = r"data.xlsx"
dns_queries = []
buffer_size = 10


domain_counts = (int)
ip_counts = (int)
query_type_counts = (int)



def process_pack(packet):
    if packet.haslayer(DNS) and packet.haslayer(DNSQR):
        dns_queries.append({
            'timestamp': datetime.fromtimestamp(packet.time).strftime('%Y-%m-%d %H:%M:%S.%f'),
            'source_ip': packet[1].src,
            'dst_ip': packet[1].dst,
            'query_name': packet[DNSQR].qname.decode() if packet[DNSQR].qname else None,
            'query_type': packet[DNSQR].qtype
        })

        if len(dns_queries) >= buffer_size:
            domain_counts[3] += 1
            ip_counts[1] += 1
            query_type_counts[4] += 1  
            save_data(dns_queries)
            dns_queries.clear() 


def save_data(dns_queries):
    
    df = pd.DataFrame(dns_queries)
    print(df)
    with pd.ExcelWriter(dns_traffic_data, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        df.to_excel(writer, index=False, header=True)
        TrafficCounts()
        plotgraph(domain_counts, ip_counts, query_type_counts)


sniff(filter="udp and port 53", prn=process_pack, count=0)
#graph.GraphTest()

