import dns.resolver
from report import make_report
import socket
import time
from datetime import datetime
from subprocess import call

output=[]
def dns_scan(domain):
    try:
        # Resolve the A record for the domain
        a_record = dns.resolver.resolve(domain, 'A')
        print(f"A record for {domain}: {', '.join([str(ip) for ip in a_record])}")
        output.append(f"A record for {domain}: {', '.join([str(ip) for ip in a_record])}")

        # Resolve the MX record for the domain
        mx_record = dns.resolver.resolve(domain, 'MX')
        print(f"MX record for {domain}: {', '.join([str(mx.exchange) for mx in mx_record])}")
        output.append(f"MX record for {domain}: {', '.join([str(mx.exchange) for mx in mx_record])}")
        for mx in mx_record:
            scan_single_ip_or_hostname(str(mx.exchange))

        # Resolve the NS record for the domain
        ns_record = dns.resolver.resolve(domain, 'NS')
        print(f"NS record for {domain}: {', '.join([str(ns.target) for ns in ns_record])}")
        output.append(f"NS record for {domain}: {', '.join([str(ns.target) for ns in ns_record])}")
        for ns in ns_record:
            scan_single_ip_or_hostname(str(ns.target))

        # Resolve the TXT record for the domain
        txt_record = dns.resolver.resolve(domain, 'TXT')
        print(f"TXT record for {domain}: {', '.join([str(txt.to_text()) for txt in txt_record])}")
        output.append(f"TXT record for {domain}: {', '.join([str(txt.to_text()) for txt in txt_record])}")

    except dns.resolver.NXDOMAIN:
        print(f"Error: {domain} does not exist.")
    except dns.resolver.Timeout:
        print(f"Error: Timeout while resolving {domain}.")
    except dns.resolver.NoAnswer:
        print(f"Error: No answer for {domain}.")
    except dns.resolver.NoNameservers:
        print(f"Error: No nameservers available for {domain}.")

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

if __name__ == "__main__":
    domain = input("Enter the domain to scan: ")
    start_time=time.time()
    dns_scan(domain)
    end_time = time.time()
    execution_time = end_time - start_time
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date = (f"Function executed in {execution_time:.6f} seconds on {current_date}")
    make_report("DNS Scanner", domain, output, "dns_report.pdf", date)
    call(["python", "run.py"])