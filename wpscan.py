import time
from datetime import datetime
import requests
import re
import sys
import urllib3
from bs4 import BeautifulSoup
from subprocess import call
from report import make_report

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

output=[]
def check_wordpress_version(url):
    try:
        response = requests.get(url, verify=False)
        if "generator" in response.text.lower():
            version = re.search(r'content="WordPress (.*?)"', response.text).group(1)
            print(f"WordPress version: {version}")
            output.append(f"WordPress version: {version}")
            return version
        else:
            print("WordPress version not found.")
            output.append("WordPress version not found.")
            return None
    except:
        print("Failed to check WordPress version.")
        return None

def check_theme_vulnerabilities(url, version):
    try:
        response = requests.get(f"{url}/wp-content/themes/", verify=False)
        if response.status_code == 200:
            print("Vulnerable themes is found!")
            output.append("Vulnerable themes is found!")
        else:
            print("No vulnerable themes found.")
            output.append("No vulnerable themes found.")
    except:
        print("Failed to check theme vulnerabilities.")

def check_interesting_headers(url):
    try:
        response = requests.get(url, verify=False)
        if "x-powered-by" in response.headers:
            print(f"X-Powered-By header: {response.headers['x-powered-by']}")
            output.append(f"X-Powered-By header: {response.headers['x-powered-by']}")
        if "server" in response.headers:
            print(f"Server header: {response.headers['server']}")
            output.append(f"Server header: {response.headers['server']}")
        if "x-frame-options" not in response.headers:
            print("X-Frame-Options header not found.")
            output.append("X-Frame-Options header not found.")
    except:
        print("Failed to check interesting headers.")

def check_wpcron_enabled(url):
    try:
        response = requests.get(f"{url}/wp-cron.php", verify=False)
        if response.status_code == 200:
            print("WP-Cron is enabled.")
            output.append("WP-Cron is enabled.")
        else:
            print("WP-Cron is not enabled.")
            output.append("WP-Cron is not enabled.")
    except:
        print("Failed to check WP-Cron status.")

def check_plugin_vulnerabilities(url, version):
    try:
        response = requests.get(f"{url}/wp-content/plugins/", verify=False)
        if response.status_code == 200:
            print("Vulnerable plugins found:")
            output.append("Vulnerable plugins found:")
            soup = BeautifulSoup(response.text, "lxml")
            plugins = soup.find_all('tr')

            # print(products)
            for plugin in plugins:
                for link in plugin.find_all('a'):
                    title = link.get('href')
                    if title:
                        print(title)
                        output.append(title)
        else:
            print("No vulnerable plugins found.")
    except:
        print("Failed to check plugin vulnerabilities.")

def check_theme_list(url):
    try:
        response = requests.get(f"{url}/wp-content/themes/", verify=False)
        if "theme-name" in response.text:
            print("Installed themes:")
            output.append("Installed themes:")
            soup = BeautifulSoup(response.text, "lxml")
            plugins = soup.find_all('tr')

            # print(products)
            for plugin in plugins:
                for link in plugin.find_all('a'):
                    title = link.get('href')
                    if title:
                        print(title)
                        output.append(title)
        else:
            print("No themes found.")
    except:
        print("Failed to check installed themes.")

def check_user_enumeration(url):
    try:
        response = requests.get(f"{url}/wp-json/wp/v2/users", verify=False)
        if response.status_code == 200:
            print("User enumeration is possible via the REST API.")
            output.append("User enumeration is possible via the REST API.")
        else:
            print("User enumeration via the REST API is not possible.")
            output.append("User enumeration is not possible via the REST API.")
    except:
        print("Failed to check user enumeration.")

def check_xmlrpc_enabled(url):
    try:
        response = requests.get(f"{url}/xmlrpc.php", verify=False)
        if response.status_code == 200:
            print("XML-RPC is enabled.")
            output.append("XML-RPC is enabled.")
        else:
            print("XML-RPC is not enabled.")
            output.append("XML-RPC is not enabled.")
    except:
        print("Failed to check XML-RPC status.")

def check_config_backups(url):
    try:
        response = requests.get(f"{url}/wp-config.php.bak", verify=False)
        if response.status_code == 200:
            print("WordPress config backup found.")
            output.append("WordPress config backup found.")
        response = requests.get(f"{url}/database.sql", verify=False)
        if response.status_code == 200:
            print("WordPress database export found.")
            output.append("WordPress database export found.")
    except:
        print("Failed to check for config backups and database exports.")

def check_timthumb_vulnerability(url, version):
    try:
        response = requests.get(f"{url}/wp-content/plugins/timthumb/timthumb.php", verify=False)
        if "TimThumb" in response.text and "Version" in response.text:
            timthumb_version = response.text.split("Version: ")[-1].split("\n")[0]
            if timthumb_version < "2.0.3":
                print(f"The TimThumb plugin version {timthumb_version} is vulnerable.")
                output.append(f"The TimThumb plugin version {timthumb_version} is vulnerable.")
        else:
            print("TimThumb plugin not found.")
            output.append("TimThumb plugin not found.")
    except:
        print("Failed to check TimThumb vulnerability.")

url = input("Enter a domain or URL: ")
url = f"https://{url}"
wordpress_version = check_wordpress_version(url)
start_time=time.time()
if wordpress_version:
    check_theme_vulnerabilities(url, wordpress_version)
    check_interesting_headers(url)
    check_wpcron_enabled(url)
    check_plugin_vulnerabilities(url, wordpress_version)
    check_theme_list(url)
    check_user_enumeration(url)
    check_xmlrpc_enabled(url)
    check_config_backups(url)
    check_timthumb_vulnerability(url, wordpress_version)
    end_time = time.time()
    execution_time = end_time - start_time
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date = (f"Function executed in {execution_time:.6f} seconds on {current_date}")
    make_report("Wordpress Scanner", url, output, "wp_report.pdf", date)
call(["python", "run.py"])