import pandas as pd
from scapy.all import DNS, DNSQR, IP, sniff
import datagraph as dg
from handler import HandleTrafficData
from openpyxl import Workbook as op
from openpyxl import load_workbook
from datetime import datetime



dns_traffic_data = r"data.xlsx"
dns_queries = []

def process_pack(packet):
    if packet.haslayer(DNS) and packet.haslayer(DNSQR):
        query = True
        dns_queries.append({
            'timestamp': datetime.fromtimestamp(packet.time).strftime('%Y-%m-%d %H:%M:%S.%f'),     
            'source_ip': packet[1].src,       
            'dst_ip': packet[1].dst,             
            'query_name': packet[DNSQR].qname.decode(),  
            'query_type': packet[DNSQR].qtype 
    })
        timestamp = datetime.fromtimestamp(dns_queries[1])
    else:
        query = False

def save_data(dns_queries):
    df = pd.DataFrame(dns_queries)
    with pd.ExcelWriter(dns_traffic_data, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        df.to_excel(writer, index=False, header=True)  

       
    



#niff(filter="udp and port 53",prn=process_pack, count=120)  
#save_data(dns_queries)
dg.graph.GraphTest()
HandleTrafficData.Read_Traffc_Data(dns_traffic_data) 
