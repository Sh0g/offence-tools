import datetime
import sys
import http.client
import requests
from bs4 import BeautifulSoup
import threading
import time
from datetime import datetime

from report import make_report

dbarray = []
url = ""
useragentdesktop = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
                    "Accept-Language": "it"}
timeoutconnection = 5
pool = None
swversion = "0.5beta"

global output
output =[]
def load_component():
    with open("comptotestdb.txt", "r") as f:
        for line in f:
            dbarray.append(line.rstrip('\n'))


def check_url(url, path="/"):
    fullurl = url + path
    try:
        conn = requests.get(fullurl, headers=useragentdesktop, timeout=timeoutconnection)
        if conn.headers["content-length"] != "0":
            return conn.status_code
        else:
            return 404
    except Exception:
        return None


def check_url_head_content_length(url, path="/"):
    fullurl = url + path
    try:
        conn = requests.head(fullurl, headers=useragentdesktop, timeout=timeoutconnection)
        return conn.headers["content-length"]
    except Exception:
        return None


def check_readme(url, component):
    if check_url(url, "/components/" + component + "/README.txt") == 200:
        print(f"\t README file found \t > {url}/components/{component}/README.txt")
        output.append(f"\t README file found \t > {url}/components/{component}/README.txt")

    if check_url(url, "/components/" + component + "/readme.txt") == 200:
        print(f"\t README file found \t > {url}/components/{component}/readme.txt")
        output.append(f"\t README file found \t > {url}/components/{component}/readme.txt")

    if check_url(url, "/components/" + component + "/README.md") == 200:
        print(f"\t README file found \t > {url}/components/{component}/README.md")
        output.append(f"\t README file found \t > {url}/components/{component}/README.md")

    if check_url(url, "/components/" + component + "/readme.md") == 200:
        print(f"\t README file found \t > {url}/components/{component}/readme.md")
        output.append(f"\t README file found \t > {url}/components/{component}/readme.md")

    if check_url(url, "/administrator/components/" + component + "/README.txt") == 200:
        print(f"\t README file found \t > {url}/administrator/components/{component}/README.txt")
        output.append(f"\t README file found \t > {url}/administrator/components/{component}/README.txt")

    if check_url(url, "/administrator/components/" + component + "/readme.txt") == 200:
        print(f"\t README file found \t > {url}/administrator/components/{component}/readme.txt")
        output.append(f"\t README file found \t > {url}/administrator/components/{component}/readme.txt")

    if check_url(url, "/administrator/components/" + component + "/README.md") == 200:
        print(f"\t README file found \t > {url}/administrator/components/{component}/README.md")
        output.append(f"\t README file found \t > {url}/administrator/components/{component}/README.md")

    if check_url(url, "/administrator/components/" + component + "/readme.md") == 200:
        print(f"\t README file found \t > {url}/administrator/components/{component}/readme.md")
        output.append(f"\t README file found \t > {url}/administrator/components/{component}/readme.md")


def check_license(url, component):
    if check_url(url, "/components/" + component + "/LICENSE.txt") == 200:
        print(f"\t LICENSE file found \t > {url}/components/{component}/LICENSE.txt")
        output.append(f"\t LICENSE file found \t > {url}/components/{component}/LICENSE.txt")

    if check_url(url, "/components/" + component + "/license.txt") == 200:
        print(f"\t LICENSE file found \t > {url}/components/{component}/license.txt")
        output.append(f"\t LICENSE file found \t > {url}/components/{component}/license.txt")

    if check_url(url, "/administrator/components/" + component + "/LICENSE.txt") == 200:
        print(f"\t LICENSE file found \t > {url}/administrator/components/{component}/LICENSE.txt")
        output.append(f"\t LICENSE file found \t > {url}/administrator/components/{component}/LICENSE.txt")

    if check_url(url, "/administrator/components/" + component + "/license.txt") == 200:
        print(f"\t LICENSE file found \t > {url}/administrator/components/{component}/license.txt")
        output.append(f"\t LICENSE file found \t > {url}/administrator/components/{component}/license.txt")

    if check_url(url, "/components/" + component + "/" + component[4:] + ".xml") == 200:
        print(f"\t LICENSE file found \t > {url}/components/{component}/{component[4:]}.xml")
        output.append(f"\t LICENSE file found \t > {url}/components/{component}/{component[4:]}.xml")

    if check_url(url, "/administrator/components/" + component + "/" + component[4:] + ".xml") == 200:
        print(f"\t LICENSE file found \t > {url}/administrator/components/{component}/{component[4:]}.xml")
        output.append(f"\t LICENSE file found \t > {url}/administrator/components/{component}/{component[4:]}.xml")


def check_changelog(url, component):
    if check_url(url, "/components/" + component + "/CHANGELOG.txt") == 200:
        print(f"\t CHANGELOG file found \t > {url}/components/{component}/CHANGELOG.txt")
        output.append(f"\t CHANGELOG file found \t > {url}/components/{component}/CHANGELOG.txt")

    if check_url(url, "/components/" + component + "/changelog.txt") == 200:
        print(f"\t CHANGELOG file found \t > {url}/components/{component}/changelog.txt")
        output.append(f"\t CHANGELOG file found \t > {url}/components/{component}/changelog.txt")

    if check_url(url, "/administrator/components/" + component + "/CHANGELOG.txt") == 200:
        print(f"\t CHANGELOG file found \t > {url}/administrator/components/{component}/CHANGELOG.txt")
        output.append(f"\t CHANGELOG file found \t > {url}/administrator/components/{component}/CHANGELOG.txt")

    if check_url(url, "/administrator/components/" + component + "/changelog.txt") == 200:
        print(f"\t CHANGELOG file found \t > {url}/administrator/components/{component}/changelog.txt")
        output.append(f"\t CHANGELOG file found \t > {url}/administrator/components/{component}/changelog.txt")


def check_mainfest(url, component):
    if check_url(url, "/components/" + component + "/MANIFEST.xml") == 200:
        print(f"\t MANIFEST file found \t > {url}/components/{component}/MANIFEST.xml")
        output.append(f"\t MANIFEST file found \t > {url}/components/{component}/MANIFEST.xml")

    if check_url(url, "/components/" + component + "/manifest.xml") == 200:
        print(f"\t MANIFEST file found \t > {url}/components/{component}/manifest.xml")
        output.append(f"\t MANIFEST file found \t > {url}/components/{component}/manifest.xml")

    if check_url(url, "/administrator/components/" + component + "/MANIFEST.xml") == 200:
        print(f"\t MANIFEST file found \t > {url}/administrator/components/{component}/MANIFEST.xml")
        output.append(f"\t MANIFEST file found \t > {url}/administrator/components/{component}/MANIFEST.xml")


    if check_url(url, "/administrator/components/" + component + "/manifest.xml") == 200:
        print(f"\t MANIFEST file found \t > {url}/administrator/components/{component}/manifest.xml")
        output.append(f"\t MANIFEST file found \t > {url}/administrator/components/{component}/manifest.xml")



def check_index(url, component):
    if check_url_head_content_length(url, "/components/" + component + "/index.htm") == 200 and int(check_url_head_content_length(url, "/components/" + component + "/index.htm")) > 1000:
        print(f"\t INDEX file descriptive found \t > {url}/components/{component}/index.htm")
        output.append(f"\t INDEX file descriptive found \t > {url}/components/{component}/index.htm")

    if check_url_head_content_length(url, "/components/" + component + "/index.html") == 200 and int(check_url_head_content_length(url, "/components/" + component + "/index.html")) > 1000:
        print(f"\t INDEX file descriptive found \t > {url}/components/{component}/index.html")
        output.append(f"\t INDEX file descriptive found \t > {url}/components/{component}/index.html")

    if check_url_head_content_length(url, "/administrator/components/" + component + "/INDEX.htm") == 200 and int(check_url_head_content_length(url, "/administrator/components/" + component + "/INDEX.htm")) > 1000:
        print(f"\t INDEX file descriptive found \t > {url}/administrator/components/{component}/INDEX.htm")
        output.append(f"\t INDEX file descriptive found \t > {url}/components/{component}/INDEX.htm")

    if check_url_head_content_length(url, "/administrator/components/" + component + "/INDEX.html") == 200 and int(check_url_head_content_length(url, "/administrator/components/" + component + "/INDEX.html")) > 1000:
        print(f"\t INDEX file descriptive found \t > {url}/administrator/components/{component}/INDEX.html")
        output.append(f"\t INDEX file descriptive found \t > {url}/components/{component}/INDEX.html")


def index_of(url, path="/"):
    fullurl = url + path
    try:
        page = requests.get(fullurl, headers=useragentdesktop, timeout=timeoutconnection)
        soup = BeautifulSoup(page.text, "html.parser")
        if soup.title:
            titlepage = soup.title.string
            if (titlepage and "Index of /" in titlepage):
                return True
            else:
                return False
        else:
            return False
    except:
        return False


def scanner(url, component):
    if check_url(url, "/index.php?option=" + component) == 200:
        print ("Component found: " + component + "\t > " + url + "/index.php?option=" + component)
        output.append("Component found: " + component + "\t > " + url + "/index.php?option=" + component)

        check_readme(url, component)

        check_license(url, component)

        check_changelog(url, component)

        check_mainfest(url, component)

        check_index(url, component)

        if index_of(url, "/components/" + component + "/"):
            print ("\t Explorable Directory \t > " + url + "/components/" + component + "/")
            output.append("\t Explorable Directory \t > " + url + "/components/" + component + "/")

        if index_of(url, "/administrator/components/" + component + "/"):
            print ("\t Explorable Directory \t > " + url + "/administrator/components/" + component + "/")
            output.append("\t Explorable Directory \t > " + url + "/administrator/components/" + component + "/")

    elif check_url(url, "/components/" + component + "/") == 200:
        print ("Component found: " + component + "\t > " + url + "/index.php?option=" + component)
        output.append("Component found: " + component + "\t > " + url + "/index.php?option=" + component)
        print ("\t But possibly it is not active or protected")
        output.append("\t But possibly it is not active or protected")

        check_readme(url, component)

        check_license(url, component)

        check_changelog(url, component)

        check_mainfest(url, component)

        check_index(url, component)

        if index_of(url, "/components/" + component + "/"):
            print ("\t Explorable Directory \t > " + url + "/components/" + component + "/")
            output.append("\t Explorable Directory \t > " + url + "/components/" + component + "/")

        if index_of(url, "/administrator/components/" + component + "/"):
            print("\t Explorable Directory \t > " + url + "/administrator/components/" + component + "/")
            output.append("\t Explorable Directory \t > " + url + "/administrator/components/" + component + "/")


    elif check_url(url, "/administrator/components/" + component + "/") == 200:
        print ("Component found: " + component + "\t > " + url + "/index.php?option=" + component)
        print ("\t On the administrator components")
        output.append("Component found: " + component + "\t > " + url + "/index.php?option=" + component)
        output.append("\t On the administrator components")

        check_readme(url, component)

        check_license(url, component)

        check_changelog(url, component)

        check_mainfest(url, component)

        check_index(url, component)

        if index_of(url, "/administrator/components/" + component + "/"):
            print ("\t Explorable Directory \t > " + url + "/components/" + component + "/")
            output.append("\t Explorable Directory \t > " + url + "/components/" + component + "/")

        if index_of(url, "/administrator/components/" + component + "/"):
            print ("\t Explorable Directory \t > " + url + "/administrator/components/" + component + "/")
            output.append("\t Explorable Directory \t > " + url + "/administrator/components/" + component + "/")


    pool.release()


def main():
    load_component()

    url = input("Enter the target URL: ")
    url = f"http://{url}"
    concurrentthreads = int(input("Enter the number of threads: "))
    start_time = time.time()
    global pool
    pool = threading.BoundedSemaphore(concurrentthreads)
    if check_url(url) != 404:

        if check_url(url, "/robots.txt") == 200:
            print( "Robots file found: \t \t > " + url + "/robots.txt")
            output.append( "Robots file found: \t \t > " + url + "/robots.txt")
        else:
            print ("No Robots file found")
            output.append("No Robots file found")

        if check_url(url, "/error_log") == 200:
            print ("Error log found: \t \t > " + url + "/error_log")
            output.append("Error log found: \t \t > " + url + "/error_log")
        else:
            print ("No Error Log found")
            output.append("No Error Log found")
        print ("\nStart scan...with %d concurrent threads!" % concurrentthreads)

        for component in dbarray:
            pool.acquire(blocking=True)

            t = threading.Thread(target=scanner, args=(url, component,))
            t.start()

        while (threading.active_count() > 1):
            time.sleep(0.1)

        print ("End Scanner")
        end_time = time.time()
        execution_time = end_time - start_time
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date = (f"Function executed in {execution_time:.6f} seconds on {current_date}")
        make_report("Joomla Scanner", url, output, "joomla_report.pdf", date)

    else:
        print ("Site Down, check url please...")


if __name__ == "__main__":
    main()