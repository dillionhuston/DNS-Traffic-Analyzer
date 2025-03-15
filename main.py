
import pandas as pd
from scapy.all import DNS, DNSQR, IP, sniff
from openpyxl import Workbook as op
from openpyxl import load_workbook
from datetime import datetime
from modules.test_module import graph
from modules.handler import update_graph
import threading#
import time#

dns_traffic_data = r"data.xlsx"
dns_queries = []
buffer_size = 10

domain_counts = {}
ip_counts = {}
query_type_counts = {}

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
            update_counts(dns_queries) 
            save_data(dns_queries) 
            dns_queries.clear()  


def update_counts(dns_queries):

    global domain_counts, ip_counts, query_type_counts

    for query in dns_queries:

        domain_name = query['query_name']
        if domain_name:
            domain_counts[domain_name] = domain_counts.get(domain_name, 0) + 1

        source_ip = query['source_ip']
        ip_counts[source_ip] = ip_counts.get(source_ip, 0) + 1

        query_type = query['query_type']
        query_type_counts[query_type] = query_type_counts.get(query_type, 0) + 1



def save_data(dns_queries):

    df = pd.DataFrame(dns_queries)
    print(df)
    with pd.ExcelWriter(dns_traffic_data, mode='w', engine='openpyxl', if_sheet_exists='replace') as writer:
        df.to_excel(writer, index=False, header=True)

def sniff_continuously():
    sniff(filter="udp and port 53", prn=process_pack, store=0)
if __name__ == "__main__":
    try:
        sniff(filter="udp and port 53", prn=process_pack, count=0)
        print("data saved to", dns_traffic_data)
        # start sniffing in a separate thread
        sniff_thread = threading.Thread(target=sniff_continuously)
        sniff_thread.daemon = True#+
        sniff_thread.start()#+

        print("DNS monitoring started. Press Ctrl+C to stop.")

        while True:
            time.sleep(10)  # wait for 10 seconds#+
            if dns_queries:#+
                update_counts(dns_queries)#+
                save_data(dns_queries)#+
                dns_queries.clear()
            update_graph()
            graph(domain_counts, ip_counts, query_type_counts)
            print("Data saved and graphs updated")

    except KeyboardInterrupt:
        print("\nDNS monitoring stopped.")
    finally:
        if dns_queries:
            update_counts(dns_queries)
            save_data(dns_queries)
        update_graph()
        graph(domain_counts, ip_counts, query_type_counts)
        print("graphs saved")
        print("press Ctrl+C to stop monitoring")
        print("Final update completed.")
   












   