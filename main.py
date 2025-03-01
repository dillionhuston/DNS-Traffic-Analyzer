from scapy.all import sniff, DNS, DNSQR, packet
#import csv libary 
import pandas as pd
import numpy as np 
import csv

def process_pack(packet):
    if packet.haslayer(DNS) and packet.haslayer(DNSQR):

        dns_query = {
            "timestamp": packet.time,
            "source": packet[1].src,
            "destination": packet[1].dst,
            "query_name": packet[DNSQR].qname.decode(),
            "query-type": packet[DNSQR].qtype
        }
        dns_quries.append(dns_query)

dns_quries = []

headers = ['time', 'b', 'c', 'd', 'e']

data_csv = open('data1.csv', 'w')
c = csv.DictWriter(data_csv, fieldnames=headers)
c.writerows(dns_quries)
data_csv.close()


sniff(filter="udp and port 53",prn=process_pack, count=0)  




