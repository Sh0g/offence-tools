import socket
import sys
import subprocess
from subprocess import call
import nmap
import time
from datetime import datetime
from report import make_report

output=[]
def scan_top_100_ports(target):
    print(f"Scanning top 100 ports on {target}")
    top_100_ports = [21, 22, 23, 25, 53, 80, 81, 88, 110, 111, 135, 139, 143, 179, 199, 389, 443, 445, 465, 514, 515, 548, 554, 587, 631, 636, 646, 873, 990, 993, 995, 1025, 1026, 1027, 1028, 1029, 1110, 1433, 1720, 1723, 1755, 1900, 2000, 2001, 2049, 2121, 2717, 3000, 3128, 3306, 3389, 3986, 4899, 5000, 5009, 5051, 5060, 5101, 5190, 5357, 5432, 5631, 5800, 5900, 6000, 6001, 6646, 7000, 7070, 8000, 8008, 8009, 8080, 8081, 8443, 8888, 9100, 9999, 10000, 32768, 49152, 49153, 49154, 49155, 49156, 49157]
    for port in top_100_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((target, port))
            if result == 0:
                print(f"Port {port} is open")
                output.append(f"Port {port} is open")
                detect_service_version(target, port)
                detect_os(target)
            sock.close()
        except:
            pass

def scan_single_ip_or_hostname(target):
    print(f"Scanning {target}")
    try:
        ip_address = socket.gethostbyname(target)
        print(f"IP address: {ip_address}")
        output.append(f"IP address: {ip_address}")
        scan_top_100_ports(ip_address)
    except socket.gaierror:
        print(f"Could not resolve hostname: {target}")
        output.append(f"Could not resolve hostname: {target}")

def scan_all_ports(target):
    print(f"Scanning all 65535 ports on {target}")
    try:
        ip_address = socket.gethostbyname(target)
        print(f"IP address: {ip_address}")
        for port in range(1, 65536):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                result = sock.connect_ex((ip_address, port))
                if result == 0:
                    print(f"Port {port} is open")
                    output.append(f"Port {port} is open")
                    detect_service_version(ip_address, port)
                    detect_os(ip_address)
                sock.close()
            except:
                pass
    except socket.gaierror:
        print(f"Could not resolve hostname: {target}")

def detect_service_version(target, port):
    print(f"Detecting service version on port {port}")
    try:
        nm = nmap.PortScanner()
        results = nm.scan(target, str(port))
        service = results['scan'][target]['tcp'][port]['name']
        version = results['scan'][target]['tcp'][port]['version']
        print(f"Service: {service}, Version: {version}")
        output.append(f"Service: {service}, Version: {version}")
    except:
        print(f"Failed to detect service version on port {port}")
        output.append(f"Failed to detect service version on port {port}")

def detect_os(target):
    print(f"Detecting operating system of {target}")
    try:
        nm = nmap.PortScanner()
        results = nm.scan(target, arguments="-O")
        os_match = results['scan'][target]['osmatch'][0]['name']
        print(f"Operating system: {os_match}")
        output.append(f"Operating system: {os_match}")
    except:
        print(f"Failed to detect operating system of {target}")
        output.append(f"Failed to detect operating system of {target}")

def traceroute(target):
    print(f"Performing traceroute to {target}")
    try:
        output = subprocess.check_output(['traceroute', target])
        print(output.decode())
    except subprocess.CalledProcessError as e:
        print(f"Failed to perform traceroute: {e}")

def main():
    target = input("Enter a domain or URL: ")
    start_time=time.time()
    scan_single_ip_or_hostname(target)
    scan_top_100_ports(target)
    end_time = time.time()
    execution_time = end_time - start_time
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date = (f"Function executed in {execution_time:.6f} seconds on {current_date}")
    make_report("Port Scanner", target, output, "portscan_report.pdf", date)
    #scan_all_ports(target)
    #traceroute(target)
    call(["python", "run.py"])

if __name__ == "__main__":
    main()