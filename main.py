from scapy.all import sniff, DNS, DNSQR, packet
#import csv libary 
import pandas as pd
import numpy as np 
import json
import pickle
import csv

def process_pack(packet):
    if packet.haslayer(DNS) and packet.haslayer(DNSQR):

        dns_query = {}
        
    
        dns_query["timestamp"] = packet.time
        dns_query["src_ip"] = packet[1].src
        dns_query["dst_ip"] = packet[1].dst
        dns_query["query_name"] = packet[DNSQR].qname.decode()
        dns_query["query_type"] = packet[DNSQR].qtype
        
        dns_queries.append(dns_query)

dns_queries = []
sniff(filter="udp and port 53",prn=process_pack, count=60)  
   
def save_to_json():
     with open('data.json', 'w') as json_file:
        json.dump(dns_queries, json_file, indent=4) 
save_to_json()




