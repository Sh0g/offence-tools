import time
from datetime import datetime
import requests
from subprocess import call
from report import make_report
import sys

output=[]
def find_subdomains(domain, subdomain_list):
    # List of common subdomains
    common_subdomains = ['www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'mobile', 'test', 'dev', 'staging', 'beta', 'demo', 'temp', 'tmp', 'backup', 'bak', 'cdn', 'cloudfront', 'app', 'blog', 'forums', 'labs', 'shop', 'store', 'jobs', 'media', 'news', 'support', 'help', 'secure', 'partners', 'learn', 'portal', 'wiki', 'web', 'api', 'service', 'services', 'apps', 'go', 'client', 'clients', 'crm', 'my', 'admin', 'staging', 'beta', 'dev', 'test', 'staging', 'beta', 'dev', 'test']

    subdomains = []

    for sub in subdomain_list:
        url = f"http://{sub}.{domain}"
        try:
            response = requests.get(url, timeout=5)
            if 200 <= response.status_code <= 299:
                subdomains.append(sub + "." + domain)
                print(f"{sub}.{domain}")
                output.append(f"{sub}.{domain}")
        except requests.exceptions.RequestException:
            pass

    return subdomains

if __name__ == "__main__":
    domain = input("Enter a domain or URL: ")
    start_time = time.time()
    with open("subdomains.txt", "r") as file:
        subdomain_list = file.read().splitlines()
    find_subdomains(domain, subdomain_list)
    output.append(f"Total is {len(output)} sites.")
    end_time = time.time()
    execution_time = end_time - start_time
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date = (f"Function executed in {execution_time:.6f} seconds on {current_date}")
    make_report("Subdomain Finder", domain, output, "sub_report.pdf", date)
    call(["python", "run.py"])