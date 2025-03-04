import pandas as pd
from scapy.all import DNS, DNSQR
from handler import HandleData
from openpyxl import Workbook as op
from openpyxl import load_workbook


dns_traffic_data = r"data.xlsx"
dns_queries = []

def process_pack(packet, load_workbook):
    if packet.haslayer(DNS) and packet.haslayer(DNSQR):
        query = True
        dns_queries.append({
            'timestamp': packet.time,            
            'dst_ip': packet[1].dst,             
            'query_name': packet[DNSQR].qname.decode(),  
            'query_type': packet[DNSQR].qtype 
    })
    else:
        query = False

def save_data(dns_queries):
    df = pd.DataFrame(dns_queries)
    with pd.ExcelWriter(dns_traffic_data, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        df.to_excel(writer, index=False, header=True)  
   

HandleData.read_data(dns_traffic_data) 
