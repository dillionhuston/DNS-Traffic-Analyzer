import openpyxl  
def handle_file():
  
    data = r'C:\Users\dillion.\Downloads\data.xlsx'
    
   
    file = openpyxl.load_workbook(data)
    ws = file.active  

    
    for row in ws.iter_rows(min_row=2, values_only=True): 
        timestamp, src_ip, dst_ip, query_name, query_type = row

        print(f"Timestamp: {timestamp}")
        print(f"Source IP: {src_ip}")
        print(f"Destination IP: {dst_ip}")
        print(f"Query Name: {query_name}")
        print(f"Query Type: {query_type}")
       
handle_file()


