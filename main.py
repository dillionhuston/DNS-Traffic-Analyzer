from scapy.all import sniff, DNS, DNSQR, packet
import pandas as pd
import numpy as np 
import json
import pickle
import csv
from openpyxl import Workbook as op
from handler import *


dns_traffic_data = r"C:\Users\dillionn\Downloads\data.xlsx"
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
        sniff(filter="udp and port 53",prn=process_pack, count=60)


def save_data(dns_queries, dns_query, query):
        
        df = pd.DataFrame(dns_queries)
        with pd.ExcelWriter(dns_traffic_data, mode='a', engine='openpyxl') as writer:
            df.to_excel(writer, index=False, header=not writer.sheets)


            print("data saved")



def test(dns_qureies):
     print(dns_queries[0])

#sniff(filter="udp and port 53", prn=process_pack, count=60)
#save_data()

test()

        

    


