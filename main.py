from scapy.all import sniff, DNS, DNSQR, packet
import pandas as pd
import numpy as np 
import json
import pickle
import csv
from openpyxl import Workbook as op
import handler 


dns_traffic_data = r"C:\Users\\Desktop\Projects\Network_monitor\Netwrok-Traffic-Analyser\data.xlsx"
dns_queries = []

def process_pack(packet):
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

        
def save_data(dns_queries, query):
        
        df = pd.DataFrame(dns_queries)
        with pd.ExcelWriter(dns_traffic_data, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
            df.to_excel(writer, index=False, header='data')
            if writer:
                print("data saved")

            query = False
            


sniff(filter="udp and port 53",prn=process_pack, count=60)
save_data(dns_queries)



        

    


